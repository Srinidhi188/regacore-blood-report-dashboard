import io
import pymupdf
from typing import Tuple, List, Optional
from app.models.report_models import Biomarker, Report
from app.parsers.date_extractor import extract_report_date
from app.parsers.biomarker_extractor import extract_biomarkers_from_text, _register_biomarker
from app.utils.logger import get_logger

logger = get_logger(__name__)

class PDFExtractionError(Exception):
    """Raised when PDF cannot be read or processed."""
    pass

def extract_text_from_pdf_stream(pdf_bytes: bytes) -> Tuple[str, List[List[str]]]:
    """
    Extracts plain text and tabular rows from PDF bytes using PyMuPDF.
    Returns: (full_text, table_rows)
    """
    full_text_list = []
    table_rows = []

    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        logger.error(f"Failed to open PDF stream: {e}")
        raise PDFExtractionError("We couldn't read this file. It might be damaged or not a valid PDF.")

    if len(doc) == 0:
        raise PDFExtractionError("The uploaded PDF file contains no pages.")

    total_text_len = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 1. Extract plain text
        page_text = page.get_text("text")
        if page_text:
            full_text_list.append(page_text)
            total_text_len += len(page_text.strip())

        # 2. Extract tables if available (PyMuPDF find_tables)
        try:
            tabs = page.find_tables()
            for tab in tabs:
                extracted = tab.extract()
                for row in extracted:
                    cleaned_row = [str(cell).strip() for cell in row if cell is not None]
                    if cleaned_row and any(cleaned_row):
                        table_rows.append(cleaned_row)
        except Exception as te:
            logger.debug(f"Table extraction on page {page_num} non-fatal notice: {te}")

    doc.close()

    full_text = "\n".join(full_text_list)

    if total_text_len < 15 and not table_rows:
        # PDF is likely scanned or image-only
        raise PDFExtractionError(
            "We couldn't extract readable text from this PDF. Please ensure it contains selectable text, or verify it is a valid digital laboratory report."
        )

    return full_text, table_rows

def parse_pdf_report(pdf_bytes: bytes, file_name: str, report_id: str) -> Report:
    """
    Orchestrates the extraction of a single blood report:
    1. Extracts text and table data
    2. Extracts report date
    3. Extracts biomarkers
    4. Bundles into a validated Report model
    """
    logger.info(f"Beginning PDF extraction for: {file_name} (ID: {report_id})")
    
    full_text, table_rows = extract_text_from_pdf_stream(pdf_bytes)
    warnings: List[str] = []

    # Extract date
    report_date, date_warning = extract_report_date(full_text)
    if date_warning:
        warnings.append(date_warning)

    # Extract biomarkers
    biomarkers = extract_biomarkers_from_text(full_text)

    # If PyMuPDF table extraction discovered additional rows
    if table_rows:
        table_text = "\n".join([" | ".join(r) for r in table_rows])
        tab_biomarkers = extract_biomarkers_from_text(table_text)
        
        existing_keys = {b.normalizedName for b in biomarkers}
        for b in tab_biomarkers:
            if b.normalizedName not in existing_keys:
                biomarkers.append(b)
                existing_keys.add(b.normalizedName)

    if not biomarkers:
        warnings.append("No recognized biomarkers could be extracted from this report.")

    raw_sample = full_text[:400] + "..." if len(full_text) > 400 else full_text

    return Report(
        id=report_id,
        fileName=file_name,
        reportDate=report_date,
        biomarkers=biomarkers,
        rawTextSample=raw_sample,
        warnings=warnings
    )
