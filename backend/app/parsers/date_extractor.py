import re
from typing import Optional, Tuple
from datetime import datetime
from dateutil import parser as date_parser

# Keyword cues ordered by priority
DATE_CUES = [
    r"(?:report\s*date|date\s*of\s*report)\s*[:\-]?\s*",
    r"(?:collection\s*date|date\s*of\s*collection|collected\s*on)\s*[:\-]?\s*",
    r"(?:sample\s*date|specimen\s*date)\s*[:\-]?\s*",
    r"(?:test\s*date|date\s*of\s*test)\s*[:\-]?\s*",
    r"(?:reported\s*on|registered\s*on)\s*[:\-]?\s*",
    r"\bdate\s*[:\-]\s*"
]

# Supported patterns
DATE_REGEX_PATTERNS = [
    # YYYY-MM-DD or YYYY/MM/DD
    r"\b(20\d{2}[-\/.](?:0[1-9]|1[0-2])[-\/.](?:0[1-9]|[12]\d|3[01]))\b",
    # DD-MM-YYYY or DD/MM/YYYY or DD.MM.YYYY
    r"\b((?:0[1-9]|[12]\d|3[01])[-\/.](?:0[1-9]|1[0-2])[-\/.](?:19|20)\d{2})\b",
    # Month Name DD, YYYY (e.g. January 15, 2026 or Jan 15, 2026 or 15 January 2026 or 15-Jan-2026)
    r"\b((?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+(?:19|20)\d{2}))\b",
    r"\b(\d{1,2}(?:st|nd|rd|th)?[\s\-]+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[\s\-]+(?:19|20)\d{2})\b"
]

def format_date_to_iso(raw_date_str: str) -> Optional[str]:
    """Attempts to parse a candidate date string into YYYY-MM-DD."""
    clean_str = raw_date_str.strip().rstrip(".,;")
    # Remove ordinal suffixes: 15th -> 15
    clean_str = re.sub(r"(\d+)(?:st|nd|rd|th)", r"\1", clean_str, flags=re.IGNORECASE)
    
    try:
        # If matches DD/MM/YYYY with day > 12, dayfirst is certain
        dt = date_parser.parse(clean_str, dayfirst=True)
        # Sanity check year
        if 1990 <= dt.year <= 2040:
            return dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    
    return None

def extract_report_date(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts report date from the PDF text.
    Returns: (iso_date_str, warning_message)
    """
    if not text or not text.strip():
        return None, "No readable text found to extract report date."

    # Pass 1: Look directly around date cues (high confidence)
    for cue in DATE_CUES:
        for pat in DATE_REGEX_PATTERNS:
            pattern = re.compile(cue + pat, re.IGNORECASE)
            match = pattern.search(text)
            if match:
                candidate = match.group(1)
                iso = format_date_to_iso(candidate)
                if iso:
                    return iso, None

    # Pass 2: Look for line items mentioning date
    lines = text.splitlines()
    for line in lines[:50]: # Header sections usually in first 50 lines
        line_lower = line.lower()
        if "date" in line_lower or "report" in line_lower:
            for pat in DATE_REGEX_PATTERNS:
                m = re.search(pat, line, re.IGNORECASE)
                if m:
                    candidate = m.group(1)
                    iso = format_date_to_iso(candidate)
                    if iso:
                        return iso, None

    # Pass 3: General scan of text for any valid date pattern (first 60 lines)
    header_chunk = "\n".join(lines[:60])
    for pat in DATE_REGEX_PATTERNS:
        matches = re.finditer(pat, header_chunk, re.IGNORECASE)
        for m in matches:
            candidate = m.group(1)
            iso = format_date_to_iso(candidate)
            if iso:
                return iso, "Date extracted from general text pattern without explicit label."

    return None, "Could not confidently identify a report date. Date set to Not Specified."
