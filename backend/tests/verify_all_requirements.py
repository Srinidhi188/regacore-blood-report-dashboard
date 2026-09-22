import os
import sys
import io
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet

BASE_URL = "http://127.0.0.1:8000"
SAMPLE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sample-reports"))

def run_all_tests():
    print("==================================================")
    print("RUNNING REGACORE COMPREHENSIVE VERIFICATION SUITE")
    print("==================================================")

    # TEST 1: Upload one PDF
    print("\n--- TEST 1: Upload 1 PDF ---")
    files_1 = [("files", ("report-1.pdf", open(f"{SAMPLE_DIR}/report-1.pdf", "rb"), "application/pdf"))]
    r1 = requests.post(f"{BASE_URL}/api/reports/analyze", files=files_1)
    assert r1.status_code == 200, f"Expected 200, got {r1.status_code}"
    d1 = r1.json()
    assert d1["summary"]["totalReports"] == 1
    assert len(d1["reports"][0]["biomarkers"]) >= 10
    print(f"PASSED: 1 PDF processed with {len(d1['reports'][0]['biomarkers'])} biomarkers.")

    # TEST 2: Upload two PDFs
    print("\n--- TEST 2: Upload 2 PDFs & Match Common Biomarkers ---")
    files_2 = [
        ("files", ("report-1.pdf", open(f"{SAMPLE_DIR}/report-1.pdf", "rb"), "application/pdf")),
        ("files", ("report-2.pdf", open(f"{SAMPLE_DIR}/report-2.pdf", "rb"), "application/pdf")),
    ]
    r2 = requests.post(f"{BASE_URL}/api/reports/analyze", files=files_2)
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["summary"]["totalReports"] == 2
    hb_2 = d2["historicalTrends"]["hemoglobin"]
    assert len(hb_2["points"]) == 2
    assert hb_2["previousValue"] == 13.2
    assert hb_2["latestValue"] == 13.5
    assert hb_2["change"] == 0.3
    print(f"PASSED: 2 PDFs matched. Hemoglobin delta calculated: {hb_2['change']} (from {hb_2['previousValue']} to {hb_2['latestValue']}).")

    # TEST 3: Upload three PDFs
    print("\n--- TEST 3: Upload 3 PDFs & Full Longitudinal Series ---")
    files_3 = [
        ("files", ("report-1.pdf", open(f"{SAMPLE_DIR}/report-1.pdf", "rb"), "application/pdf")),
        ("files", ("report-2.pdf", open(f"{SAMPLE_DIR}/report-2.pdf", "rb"), "application/pdf")),
        ("files", ("report-3.pdf", open(f"{SAMPLE_DIR}/report-3.pdf", "rb"), "application/pdf")),
    ]
    r3 = requests.post(f"{BASE_URL}/api/reports/analyze", files=files_3)
    assert r3.status_code == 200
    d3 = r3.json()
    assert d3["summary"]["totalReports"] == 3
    for key in ["hemoglobin", "fasting_glucose", "total_cholesterol", "vitamin_d"]:
        trend = d3["historicalTrends"][key]
        assert len(trend["points"]) == 3, f"Expected 3 points for {key}, got {len(trend['points'])}"
        print(f"  [OK] {trend['displayName']}: {[p['value'] for p in trend['points']]}")
    print("PASSED: 3 PDFs produced 3-point time-series across all common biomarkers.")

    # TEST 4: Upload invalid file
    print("\n--- TEST 4: Upload Invalid File ---")
    r4 = requests.post(
        f"{BASE_URL}/api/reports/analyze",
        files=[("files", ("corrupt.txt", b"Random text not a pdf", "text/plain"))]
    )
    assert r4.status_code == 422
    err_detail = r4.json()["detail"]
    assert "couldn't extract readable data" in err_detail
    print(f"PASSED: Invalid file rejected with friendly message: '{err_detail}'")

    # TEST 5: Upload PDF with missing reference range
    print("\n--- TEST 5: Upload PDF with Missing Reference Range ---")
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("<b>CLINICAL REPORT</b>", styles["Heading1"]),
        Paragraph("Report Date: 2026-05-01", styles["Normal"]),
        Paragraph("Hemoglobin: 14.1 g/dL", styles["Normal"])  # No reference range specified
    ]
    doc.build(story)
    buf.seek(0)

    r5 = requests.post(
        f"{BASE_URL}/api/reports/analyze",
        files=[("files", ("no_range.pdf", buf.getvalue(), "application/pdf"))]
    )
    assert r5.status_code == 200
    d5 = r5.json()
    hb_item = d5["historicalTrends"]["hemoglobin"]
    assert hb_item["referenceRange"] is None
    print(f"PASSED: Missing reference range safely processed without error. ReferenceRange: {hb_item['referenceRange']}")

    # TEST 6: Upload report with missing biomarker (ensure no invented fake values)
    print("\n--- TEST 6: Upload Report with Missing Biomarker ---")
    buf2 = io.BytesIO()
    doc2 = SimpleDocTemplate(buf2)
    story2 = [
        Paragraph("<b>PARTIAL BLOOD TEST</b>", styles["Heading1"]),
        Paragraph("Report Date: 2026-07-01", styles["Normal"]),
        Paragraph("Fasting Glucose: 99 mg/dL (70-99)", styles["Normal"]) # Only glucose, NO Hemoglobin
    ]
    doc2.build(story2)
    buf2.seek(0)

    files_6 = [
        ("files", ("report-1.pdf", open(f"{SAMPLE_DIR}/report-1.pdf", "rb"), "application/pdf")),
        ("files", ("partial.pdf", buf2.getvalue(), "application/pdf")),
    ]
    r6 = requests.post(f"{BASE_URL}/api/reports/analyze", files=files_6)
    assert r6.status_code == 200
    d6 = r6.json()
    # Glucose should have 2 points (report-1 + partial)
    assert len(d6["historicalTrends"]["fasting_glucose"]["points"]) == 2
    # Hemoglobin should have ONLY 1 point (from report-1), NO fake value invented for partial.pdf!
    assert len(d6["historicalTrends"]["hemoglobin"]["points"]) == 1
    print(f"PASSED: Hemoglobin has only 1 point, Glucose has 2 points. No hallucinated/invented data.")

    # TEST 7: Backend Health Check
    print("\n--- TEST 7: Backend Health & System Uptime ---")
    r7 = requests.get(f"{BASE_URL}/api/health")
    assert r7.status_code == 200
    print(f"PASSED: Health response: {r7.json()}")

    print("\n==================================================")
    print("ALL 7 MANDATORY VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run_all_tests()
