import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

def test_api_endpoints():
    client = TestClient(app)
    
    # 1. Health check
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    print("Health check status:", res_health.json())

    # 2. Sample data endpoint
    res_sample = client.get("/api/reports/sample-data")
    assert res_sample.status_code == 200
    sample_json = res_sample.json()
    print("Sample data total reports:", sample_json["summary"]["totalReports"])
    print("Sample data unique biomarkers:", sample_json["summary"]["uniqueBiomarkers"])
    assert sample_json["summary"]["totalReports"] == 3

    # 3. Analyze endpoint with real files
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sample-reports"))
    files_to_upload = [
        ("files", ("report-1.pdf", open(os.path.join(sample_dir, "report-1.pdf"), "rb"), "application/pdf")),
        ("files", ("report-2.pdf", open(os.path.join(sample_dir, "report-2.pdf"), "rb"), "application/pdf")),
        ("files", ("report-3.pdf", open(os.path.join(sample_dir, "report-3.pdf"), "rb"), "application/pdf")),
    ]
    res_analyze = client.post("/api/reports/analyze", files=files_to_upload)
    assert res_analyze.status_code == 200
    analyze_json = res_analyze.json()
    print("Analyze endpoint total reports:", analyze_json["summary"]["totalReports"])
    print("Analyze endpoint biomarkers table rows:", len(analyze_json["biomarkersTable"]))
    assert analyze_json["summary"]["totalReports"] == 3
    assert "hemoglobin" in analyze_json["historicalTrends"]
    
    # 4. Error testing: upload non-pdf
    res_err = client.post("/api/reports/analyze", files=[
        ("files", ("test.txt", b"invalid file content", "text/plain"))
    ])
    assert res_err.status_code == 422
    print("Invalid upload test error response received properly:", res_err.json())

    print("\nALL FASTAPI ENDPOINT TESTS PASSED!")

if __name__ == "__main__":
    test_api_endpoints()
