import os
import uuid
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from app.models.report_models import AnalyzeResponse, Report
from app.parsers.pdf_parser import parse_pdf_report, PDFExtractionError
from app.services.history_service import build_analysis_response
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/reports", tags=["Reports"])

# Path to sample reports directory
SAMPLE_REPORTS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "sample-reports")
)

@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyze one or more blood report PDF files"
)
async def analyze_reports(files: List[UploadFile] = File(...)):
    """
    Accepts one or more PDF blood test reports, extracts text and tabular data,
    normalizes biomarkers, extracts dates, organizes historical time series,
    and returns a structured dashboard payload.
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide at least one PDF blood report file to analyze."
        )

    parsed_reports: List[Report] = []
    warnings: List[str] = []

    for file_obj in files:
        filename = file_obj.filename or "unknown.pdf"
        
        # Verify extension
        if not filename.lower().endswith(".pdf"):
            warnings.append(f"File '{filename}' was skipped because only PDF files are supported.")
            continue

        try:
            content = await file_obj.read()
            if not content or len(content) == 0:
                warnings.append(f"File '{filename}' is empty.")
                continue

            report_id = f"rep_{uuid.uuid4().hex[:8]}"
            report = parse_pdf_report(pdf_bytes=content, file_name=filename, report_id=report_id)
            parsed_reports.append(report)

        except PDFExtractionError as pe:
            logger.warning(f"PDF extraction error on {filename}: {pe}")
            warnings.append(f"{filename}: {str(pe)}")
        except Exception as e:
            logger.error(f"Unexpected error processing {filename}: {e}", exc_info=True)
            warnings.append(
                f"We encountered an issue processing '{filename}'. Please verify that it is an uncorrupted blood report PDF."
            )

    if not parsed_reports:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "We couldn't extract readable data from the uploaded file(s). "
                "Please verify that the files are valid digital blood reports containing text."
            )
        )

    response = build_analysis_response(parsed_reports, initial_warnings=warnings)
    return response

@router.get(
    "/sample-data",
    response_model=AnalyzeResponse,
    summary="Get pre-processed analysis from the standard sample blood reports"
)
async def get_sample_reports_data():
    """
    Directly processes the 3 built-in sample reports to provide an instant
    demonstration experience for the dashboard evaluator.
    """
    sample_files = ["report-1.pdf", "report-2.pdf", "report-3.pdf"]
    parsed_reports: List[Report] = []
    warnings: List[str] = []

    for s_file in sample_files:
        full_path = os.path.join(SAMPLE_REPORTS_DIR, s_file)
        if not os.path.exists(full_path):
            warnings.append(f"Sample file '{s_file}' not found in sample directory.")
            continue

        try:
            with open(full_path, "rb") as f:
                content = f.read()
            report_id = f"sample_{s_file.replace('.pdf', '')}"
            report = parse_pdf_report(pdf_bytes=content, file_name=s_file, report_id=report_id)
            parsed_reports.append(report)
        except Exception as e:
            logger.error(f"Error loading sample report {s_file}: {e}")
            warnings.append(f"Could not load sample report {s_file}.")

    if not parsed_reports:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sample reports have not been generated yet. Please trigger sample generation."
        )

    return build_analysis_response(parsed_reports, initial_warnings=warnings)

@router.get("/download-sample/{filename}")
async def download_sample_report(filename: str):
    """Allows downloading a sample report PDF directly for manual upload testing."""
    safe_name = os.path.basename(filename)
    full_path = os.path.join(SAMPLE_REPORTS_DIR, safe_name)
    if not os.path.exists(full_path) or not safe_name.endswith(".pdf"):
        raise HTTPException(status_code=404, detail="Sample PDF not found.")
    return FileResponse(
        path=full_path,
        media_type="application/pdf",
        filename=safe_name
    )
