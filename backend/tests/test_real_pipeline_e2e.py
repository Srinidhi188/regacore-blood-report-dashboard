import os
import sys
import json
import requests

BASE_URL = "http://127.0.0.1:8000"
SAMPLE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sample-reports"))

def test_full_pipeline():
    print("=" * 60)
    print("REGACORE FINAL E2E PIPELINE VERIFICATION")
    print("=" * 60)

    # 1. Verify files exist
    files = ["sample-report-1.pdf", "sample-report-2.pdf", "sample-report-3.pdf"]
    for f in files:
        path = os.path.join(SAMPLE_DIR, f)
        assert os.path.exists(path), f"Missing {f} at {path}"
        print(f"File verified: {f} ({os.path.getsize(path)} bytes)")

    # ----------------------------------------------------
    # STEP 1: Upload sample-report-1.pdf (Single Report)
    # ----------------------------------------------------
    print("\n>>> STEP 1: Uploading sample-report-1.pdf (Single Report)...")
    with open(os.path.join(SAMPLE_DIR, "sample-report-1.pdf"), "rb") as fp1:
        upload_data = [("files", ("sample-report-1.pdf", fp1, "application/pdf"))]
        res1 = requests.post(f"{BASE_URL}/api/reports/analyze", files=upload_data)
    
    assert res1.status_code == 200, f"Expected 200, got {res1.status_code}: {res1.text}"
    d1 = res1.json()
    assert d1["summary"]["totalReports"] == 1
    assert d1["summary"]["latestReportDate"] == "2026-01-15"
    assert len(d1["reports"]) == 1
    r1 = d1["reports"][0]
    assert r1["fileName"] == "sample-report-1.pdf"
    assert r1["reportDate"] == "2026-01-15"
    assert len(r1["biomarkers"]) == 12
    print(f"  [PASS] Report 1 extracted: Date={r1['reportDate']}, Biomarkers Count={len(r1['biomarkers'])}")
    for b in r1["biomarkers"]:
        print(f"    - {b['displayName']}: {b['value']} {b['unit']} (Ref: {b['referenceRange']})")

    # ----------------------------------------------------
    # STEP 2: Upload sample-report-1.pdf + sample-report-2.pdf (Two Reports Matching)
    # ----------------------------------------------------
    print("\n>>> STEP 2: Uploading sample-report-1.pdf + sample-report-2.pdf (Matching Biomarkers)...")
    with open(os.path.join(SAMPLE_DIR, "sample-report-1.pdf"), "rb") as fp1, \
         open(os.path.join(SAMPLE_DIR, "sample-report-2.pdf"), "rb") as fp2:
        upload_data = [
            ("files", ("sample-report-1.pdf", fp1, "application/pdf")),
            ("files", ("sample-report-2.pdf", fp2, "application/pdf"))
        ]
        res2 = requests.post(f"{BASE_URL}/api/reports/analyze", files=upload_data)
    
    assert res2.status_code == 200
    d2 = res2.json()
    assert d2["summary"]["totalReports"] == 2
    assert d2["summary"]["earliestReportDate"] == "2026-01-15"
    assert d2["summary"]["latestReportDate"] == "2026-03-20"
    
    # Verify common biomarkers matched
    hb_trend = d2["historicalTrends"]["hemoglobin"]
    assert len(hb_trend["points"]) == 2
    assert hb_trend["previousValue"] == 13.2
    assert hb_trend["latestValue"] == 13.5
    assert hb_trend["change"] == 0.3
    print(f"  [PASS] Two reports matched. Hemoglobin change: {hb_trend['change']} ({hb_trend['previousValue']} -> {hb_trend['latestValue']})")
    
    glu_trend = d2["historicalTrends"]["fasting_glucose"]
    assert len(glu_trend["points"]) == 2
    assert glu_trend["previousValue"] == 96.0
    assert glu_trend["latestValue"] == 102.0
    assert glu_trend["change"] == 6.0
    print(f"  [PASS] Glucose matched. Change: +{glu_trend['change']} ({glu_trend['previousValue']} -> {glu_trend['latestValue']})")

    # ----------------------------------------------------
    # STEP 3: Upload sample-report-1 + sample-report-2 + sample-report-3 (All Three)
    # ----------------------------------------------------
    print("\n>>> STEP 3: Uploading all 3 sample reports (Full Longitudinal Timeline)...")
    with open(os.path.join(SAMPLE_DIR, "sample-report-1.pdf"), "rb") as fp1, \
         open(os.path.join(SAMPLE_DIR, "sample-report-2.pdf"), "rb") as fp2, \
         open(os.path.join(SAMPLE_DIR, "sample-report-3.pdf"), "rb") as fp3:
        upload_data = [
            ("files", ("sample-report-1.pdf", fp1, "application/pdf")),
            ("files", ("sample-report-2.pdf", fp2, "application/pdf")),
            ("files", ("sample-report-3.pdf", fp3, "application/pdf"))
        ]
        res3 = requests.post(f"{BASE_URL}/api/reports/analyze", files=upload_data)
    
    assert res3.status_code == 200
    d3 = res3.json()
    assert d3["summary"]["totalReports"] == 3
    assert d3["summary"]["uniqueBiomarkers"] == 12
    assert d3["summary"]["earliestReportDate"] == "2026-01-15"
    assert d3["summary"]["latestReportDate"] == "2026-06-10"
    assert d3["summary"]["dateRangeText"] == "2026-01-15 to 2026-06-10"
    print(f"  [PASS] All 3 dates verified: {d3['summary']['dateRangeText']}")

    # Verify all 12 biomarkers have 3 historical points
    print("\n>>> STEP 4: Verifying 3 Extracted Historical Points for All 12 Biomarkers:")
    expected_keys = [
        "hemoglobin", "fasting_glucose", "total_cholesterol", "hdl_cholesterol",
        "ldl_cholesterol", "triglycerides", "vitamin_d", "creatinine",
        "blood_urea_nitrogen", "wbc", "rbc", "platelets"
    ]
    
    for key in expected_keys:
        assert key in d3["historicalTrends"], f"Missing {key} in historicalTrends"
        trend = d3["historicalTrends"][key]
        assert len(trend["points"]) == 3, f"Expected 3 points for {key}, got {len(trend['points'])}"
        pts_str = " -> ".join([f"{p['reportDate']}: {p['value']} {p['unit']}" for p in trend["points"]])
        print(f"  [PASS] {trend['displayName']:28}: {pts_str} | Prev={trend['previousValue']} Latest={trend['latestValue']} Change={trend['change']}")

    # ----------------------------------------------------
    # STEP 5: Verify Biomarker Comparison Table
    # ----------------------------------------------------
    print("\n>>> STEP 5: Verifying Biomarker Comparison Table Data:")
    table_rows = d3["biomarkersTable"]
    assert len(table_rows) == 12
    for row in table_rows:
        assert row["latestValue"] is not None
        assert row["unit"] is not None
        assert row["referenceRange"] is not None
        assert row["latestReportDate"] == "2026-06-10"
        print(f"  [PASS] Table Row: {row['displayName']:28} | Latest: {row['latestValue']} {row['unit']} | Ref: {row['referenceRange']} | Prev: {row['previousValue']} | Delta: {row['change']}")

    # ----------------------------------------------------
    # STEP 6: Verify Report History List
    # ----------------------------------------------------
    print("\n>>> STEP 6: Verifying Report History List:")
    assert len(d3["reports"]) == 3
    report_names = [r["fileName"] for r in d3["reports"]]
    assert "sample-report-1.pdf" in report_names
    assert "sample-report-2.pdf" in report_names
    assert "sample-report-3.pdf" in report_names
    for r in d3["reports"]:
        print(f"  [PASS] Report History Item: {r['fileName']} on {r['reportDate']} with {len(r['biomarkers'])} biomarkers")

    # ----------------------------------------------------
    # STEP 7: Test Invalid / Non-PDF File Rejection
    # ----------------------------------------------------
    print("\n>>> STEP 7: Testing Invalid Non-PDF File Upload Rejection:")
    bad_upload = [("files", ("not_a_report.txt", b"Hello, this is just plain text, not a PDF report.", "text/plain"))]
    res_bad = requests.post(f"{BASE_URL}/api/reports/analyze", files=bad_upload)
    assert res_bad.status_code == 422
    err_detail = res_bad.json()["detail"]
    assert "couldn't extract readable data" in err_detail
    print(f"  [PASS] Application properly rejected non-PDF with friendly message:\n         '{err_detail}'")

    print("\n" + "=" * 60)
    print("SUCCESS: REAL PDF UPLOAD & EXTRACTION PIPELINE FULLY VERIFIED END-TO-END!")
    print("=" * 60)

if __name__ == "__main__":
    test_full_pipeline()
