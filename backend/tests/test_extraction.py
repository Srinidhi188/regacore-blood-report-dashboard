import os
import sys

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.parsers.pdf_parser import parse_pdf_report
from app.services.history_service import build_analysis_response

def test_pipeline():
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sample-reports"))
    files = ["report-1.pdf", "report-2.pdf", "report-3.pdf"]
    parsed_reports = []

    print("=== Testing PDF Extraction & Date Parsing ===")
    for f in files:
        path = os.path.join(sample_dir, f)
        with open(path, "rb") as fp:
            content = fp.read()
        rep = parse_pdf_report(content, f, f"id_{f}")
        print(f"\nFile: {f}")
        print(f"Extracted Date: {rep.reportDate}")
        print(f"Extracted Biomarkers Count: {len(rep.biomarkers)}")
        for bm in rep.biomarkers[:5]:
            print(f"  - {bm.displayName} ({bm.normalizedName}): {bm.value} {bm.unit} [Range: {bm.referenceRange}]")
        parsed_reports.append(rep)

    print("\n=== Testing Historical Matching & Aggregation ===")
    response = build_analysis_response(parsed_reports)
    print(f"Total Reports: {response.summary.totalReports}")
    print(f"Unique Biomarkers: {response.summary.uniqueBiomarkers}")
    print(f"Date Range: {response.summary.dateRangeText}")

    # Check hemoglobin trend
    hb_history = response.historicalTrends.get("hemoglobin")
    if hb_history:
        print(f"\nHemoglobin Trend ({hb_history.displayName}):")
        print(f"  Latest Value: {hb_history.latestValue} {hb_history.unit}")
        print(f"  Previous Value: {hb_history.previousValue}")
        print(f"  Change: {hb_history.change}")
        for pt in hb_history.points:
            print(f"    Date: {pt.reportDate} -> Value: {pt.value}")

    # Check vitamin D trend
    vitd_history = response.historicalTrends.get("vitamin_d")
    if vitd_history:
        print(f"\nVitamin D Trend ({vitd_history.displayName}):")
        print(f"  Latest Value: {vitd_history.latestValue} {vitd_history.unit}")
        print(f"  Previous Value: {vitd_history.previousValue}")
        print(f"  Change: {vitd_history.change}")
        for pt in vitd_history.points:
            print(f"    Date: {pt.reportDate} -> Value: {pt.value}")

    assert response.summary.totalReports == 3, "Expected 3 reports"
    assert len(response.historicalTrends) >= 10, "Expected at least 10 normalized biomarkers"
    print("\nALL BACKEND EXTRACTION & HISTORICAL MATCHING TESTS PASSED!")

if __name__ == "__main__":
    test_pipeline()
