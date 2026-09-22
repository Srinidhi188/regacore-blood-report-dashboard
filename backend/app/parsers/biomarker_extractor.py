import re
from typing import List, Optional, Tuple, Dict
from app.models.report_models import Biomarker
from app.services.normalization import (
    normalize_biomarker_name,
    parse_reference_range,
    determine_status,
    clean_biomarker_text,
    BIOMARKER_ALIASES
)
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Common medical test units
COMMON_UNITS = [
    r"g/dL", r"mg/dL", r"ng/mL", r"pg/mL", r"mmol/L", r"µIU/mL", r"uIU/mL", r"mIU/L",
    r"10\^3/µL", r"10\^3/uL", r"10\^6/µL", r"10\^6/uL", r"x10\^3/uL", r"x10\^6/uL",
    r"/cumm", r"cells/cu\.mm", r"cells/uL", r"/uL", r"%", r"fL", r"pg", r"U/L", r"IU/L",
    r"mEq/L", r"mg/L", r"ug/dL", r"µg/dL", r"sec", r"seconds", r"ratio"
]
UNITS_REGEX = r"(?:" + "|".join(COMMON_UNITS) + r")"

# Lines or headers to ignore
IGNORE_KEYWORDS = [
    "patient", "doctor", "physician", "hospital", "clinic", "laboratory", "address",
    "phone", "email", "collected", "reported", "specimen", "page", "test name",
    "investigation", "observed value", "reference range", "normal range", "units",
    "method", "technology", "interpretation", "note", "signature", "end of report",
    "sample / demonstration", "apex diagnostic", "date of report", "age", "gender",
    "sex", "barcode", "patient id", "mrn", "sample type", "referred by", "status: final"
]

def is_ignorable_line(line: str) -> bool:
    line_lower = line.strip().lower()
    if not line_lower or len(line_lower) < 3:
        return True
    for kw in IGNORE_KEYWORDS:
        if kw in line_lower and not any(alias in line_lower for alias in ["hb", "wbc", "rbc", "alt", "ast", "bun", "tsh"]):
            # Check if it's purely header/metadata line
            if len(line_lower.split()) < 6 or "sample / demonstration" in line_lower:
                return True
    return False

def parse_numeric_value(val_str: str) -> Optional[float]:
    """Extracts float value from raw string, handling < or > prefixes."""
    clean = re.sub(r"[<>=]", "", val_str).strip()
    # Remove thousand separators
    clean = clean.replace(",", "")
    try:
        return float(clean)
    except ValueError:
        return None

def extract_biomarkers_from_text(text: str) -> List[Biomarker]:
    """
    Parses biomarkers from extracted text using multiple complementary strategies:
    1. Delimited / pipe table rows
    2. Space/tab structured row patterns
    3. Anchor-based alias searches
    """
    biomarkers_dict: Dict[str, Biomarker] = {}
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # Strategy 1: Delimited lines (e.g. "Hemoglobin | 13.5 | g/dL | 12.0 - 16.0")
    for line in lines:
        if "|" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                name_cand = parts[0]
                if is_ignorable_line(name_cand):
                    continue
                val_cand = parts[1]
                num_val = parse_numeric_value(val_cand)
                if num_val is not None:
                    unit_cand = parts[2] if len(parts) > 2 else None
                    ref_cand = parts[3] if len(parts) > 3 else None
                    _register_biomarker(biomarkers_dict, name_cand, num_val, unit_cand, ref_cand)

    # Strategy 2: Regex for Structured Rows
    # Format: [Biomarker Name] [Value] [Unit] [Reference Range (optional)]
    row_pattern = re.compile(
        rf"^([A-Za-z0-9\s\(\)\/\-\,\.]+?)\s+([<>]?\s*\d+(?:\.\d+)?)\s+({UNITS_REGEX})\s*(.*)$",
        re.IGNORECASE
    )

    for line in lines:
        if line.startswith("#") or is_ignorable_line(line):
            continue
        match = row_pattern.match(line)
        if match:
            raw_name = match.group(1).strip()
            raw_val = match.group(2).strip()
            unit = match.group(3).strip()
            ref_part = match.group(4).strip() if match.group(4) else None

            num_val = parse_numeric_value(raw_val)
            if num_val is not None and not is_ignorable_line(raw_name):
                _register_biomarker(biomarkers_dict, raw_name, num_val, unit, ref_part)

    # Strategy 3: Key-Value format (e.g. "Hemoglobin: 13.5 g/dL (Ref: 12.0 - 16.0)")
    kv_pattern = re.compile(
        rf"^([A-Za-z0-9\s\(\)\/\-\,\.]+?)\s*[:=]\s*([<>]?\s*\d+(?:\.\d+)?)\s*({UNITS_REGEX})?(?:\s*[\(\[]?(?:ref|reference|normal)?\s*[:\-]?\s*([0-9\.\-\–\s\<\>]+)[\)\]]?)?",
        re.IGNORECASE
    )

    for line in lines:
        if line.startswith("#") or is_ignorable_line(line):
            continue
        m = kv_pattern.match(line)
        if m:
            raw_name = m.group(1).strip()
            raw_val = m.group(2).strip()
            unit = m.group(3).strip() if m.group(3) else None
            ref_part = m.group(4).strip() if m.group(4) else None
            num_val = parse_numeric_value(raw_val)
            if num_val is not None and not is_ignorable_line(raw_name):
                _register_biomarker(biomarkers_dict, raw_name, num_val, unit, ref_part)

    # Strategy 4: Anchor search for common lab biomarkers if not detected yet
    for alias in BIOMARKER_ALIASES.keys():
        if len(alias) < 3 and alias not in ["hb", "tg", "tc"]:
            continue
        pattern = re.compile(
            rf"\b({re.escape(alias)})\b\s*[:\-]?\s*([<>]?\s*\d+(?:\.\d+)?)\s*({UNITS_REGEX})?\s*([0-9\.\-\–\<\>\s]+)?",
            re.IGNORECASE
        )
        for line in lines:
            m = pattern.search(line)
            if m:
                raw_name = m.group(1).strip()
                raw_val = m.group(2).strip()
                unit = m.group(3).strip() if m.group(3) else None
                ref_part = m.group(4).strip() if m.group(4) else None
                num_val = parse_numeric_value(raw_val)
                if num_val is not None:
                    _register_biomarker(biomarkers_dict, raw_name, num_val, unit, ref_part)

    return list(biomarkers_dict.values())

def _register_biomarker(
    biomarkers_dict: Dict[str, Biomarker],
    raw_name: str,
    value: float,
    unit: Optional[str],
    reference_range: Optional[str]
):
    """Normalizes and safely records biomarker if valid."""
    cleaned_name = clean_biomarker_text(raw_name)
    if not cleaned_name or len(cleaned_name) < 2:
        return

    normalized_key, display_name, category = normalize_biomarker_name(cleaned_name)
    
    # If already recorded, only overwrite if current has richer info (e.g. unit/ref)
    if normalized_key in biomarkers_dict:
        existing = biomarkers_dict[normalized_key]
        if not existing.referenceRange and reference_range:
            existing.referenceRange = reference_range.strip()
            ref_low, ref_high = parse_reference_range(existing.referenceRange)
            existing.refLow = ref_low
            existing.refHigh = ref_high
            existing.status = determine_status(existing.value, ref_low, ref_high)
        if not existing.unit and unit:
            existing.unit = unit.strip()
        return

    clean_ref = reference_range.strip() if reference_range else None
    ref_low, ref_high = parse_reference_range(clean_ref)
    status = determine_status(value, ref_low, ref_high)

    bm = Biomarker(
        name=cleaned_name,
        normalizedName=normalized_key,
        displayName=display_name,
        value=value,
        unit=unit.strip() if unit else None,
        referenceRange=clean_ref,
        category=category,
        status=status,
        refLow=ref_low,
        refHigh=ref_high
    )
    biomarkers_dict[normalized_key] = bm
