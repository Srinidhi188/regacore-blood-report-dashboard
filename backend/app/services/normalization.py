import re
from typing import Tuple, Optional, Dict, Any

# Canonical dictionary metadata: normalized_key -> {display_name, category, default_unit}
BIOMARKER_CANONICAL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "hemoglobin": {
        "displayName": "Hemoglobin",
        "category": "Complete Blood Count",
        "defaultUnit": "g/dL"
    },
    "fasting_glucose": {
        "displayName": "Fasting Blood Glucose",
        "category": "Metabolic Panel",
        "defaultUnit": "mg/dL"
    },
    "total_cholesterol": {
        "displayName": "Total Cholesterol",
        "category": "Lipid Profile",
        "defaultUnit": "mg/dL"
    },
    "hdl_cholesterol": {
        "displayName": "HDL Cholesterol",
        "category": "Lipid Profile",
        "defaultUnit": "mg/dL"
    },
    "ldl_cholesterol": {
        "displayName": "LDL Cholesterol",
        "category": "Lipid Profile",
        "defaultUnit": "mg/dL"
    },
    "triglycerides": {
        "displayName": "Triglycerides",
        "category": "Lipid Profile",
        "defaultUnit": "mg/dL"
    },
    "vldl_cholesterol": {
        "displayName": "VLDL Cholesterol",
        "category": "Lipid Profile",
        "defaultUnit": "mg/dL"
    },
    "vitamin_d": {
        "displayName": "Vitamin D (25-OH)",
        "category": "Vitamins & Minerals",
        "defaultUnit": "ng/mL"
    },
    "creatinine": {
        "displayName": "Serum Creatinine",
        "category": "Renal Function",
        "defaultUnit": "mg/dL"
    },
    "blood_urea_nitrogen": {
        "displayName": "Blood Urea Nitrogen (BUN)",
        "category": "Renal Function",
        "defaultUnit": "mg/dL"
    },
    "wbc": {
        "displayName": "White Blood Cell Count (WBC)",
        "category": "Complete Blood Count",
        "defaultUnit": "10^3/µL"
    },
    "rbc": {
        "displayName": "Red Blood Cell Count (RBC)",
        "category": "Complete Blood Count",
        "defaultUnit": "10^6/µL"
    },
    "platelets": {
        "displayName": "Platelet Count",
        "category": "Complete Blood Count",
        "defaultUnit": "10^3/µL"
    },
    "hematocrit": {
        "displayName": "Hematocrit (PCV)",
        "category": "Complete Blood Count",
        "defaultUnit": "%"
    },
    "mcv": {
        "displayName": "Mean Corpuscular Volume (MCV)",
        "category": "Complete Blood Count",
        "defaultUnit": "fL"
    },
    "mch": {
        "displayName": "Mean Corpuscular Hemoglobin (MCH)",
        "category": "Complete Blood Count",
        "defaultUnit": "pg"
    },
    "mchc": {
        "displayName": "MCHC",
        "category": "Complete Blood Count",
        "defaultUnit": "g/dL"
    },
    "hba1c": {
        "displayName": "HbA1c (Glycated Hemoglobin)",
        "category": "Metabolic Panel",
        "defaultUnit": "%"
    },
    "alt": {
        "displayName": "ALT (SGPT)",
        "category": "Liver Function",
        "defaultUnit": "U/L"
    },
    "ast": {
        "displayName": "AST (SGOT)",
        "category": "Liver Function",
        "defaultUnit": "U/L"
    },
    "bilirubin_total": {
        "displayName": "Total Bilirubin",
        "category": "Liver Function",
        "defaultUnit": "mg/dL"
    },
    "albumin": {
        "displayName": "Serum Albumin",
        "category": "Liver Function",
        "defaultUnit": "g/dL"
    },
    "total_protein": {
        "displayName": "Total Protein",
        "category": "Liver Function",
        "defaultUnit": "g/dL"
    },
    "tsh": {
        "displayName": "TSH (Thyroid Stimulating Hormone)",
        "category": "Thyroid",
        "defaultUnit": "µIU/mL"
    },
    "calcium": {
        "displayName": "Calcium",
        "category": "Metabolic Panel",
        "defaultUnit": "mg/dL"
    },
    "potassium": {
        "displayName": "Potassium",
        "category": "Electrolytes",
        "defaultUnit": "mEq/L"
    },
    "sodium": {
        "displayName": "Sodium",
        "category": "Electrolytes",
        "defaultUnit": "mEq/L"
    }
}

# Alias mapping table to normalized key
BIOMARKER_ALIASES: Dict[str, str] = {
    # Hemoglobin
    "hb": "hemoglobin",
    "hgb": "hemoglobin",
    "hemoglobin": "hemoglobin",
    "haemoglobin": "hemoglobin",
    "total hemoglobin": "hemoglobin",
    
    # Fasting Glucose / Blood Sugar
    "fbs": "fasting_glucose",
    "glucose": "fasting_glucose",
    "fasting glucose": "fasting_glucose",
    "fasting blood sugar": "fasting_glucose",
    "blood sugar (fasting)": "fasting_glucose",
    "blood glucose (fasting)": "fasting_glucose",
    "fasting blood glucose": "fasting_glucose",
    "fpg": "fasting_glucose",
    "glu": "fasting_glucose",
    
    # Cholesterol
    "total cholesterol": "total_cholesterol",
    "cholesterol total": "total_cholesterol",
    "cholesterol": "total_cholesterol",
    "tc": "total_cholesterol",
    "tchol": "total_cholesterol",
    "serum cholesterol": "total_cholesterol",
    
    # HDL
    "hdl": "hdl_cholesterol",
    "hdl cholesterol": "hdl_cholesterol",
    "hdl-cholesterol": "hdl_cholesterol",
    "hdl-c": "hdl_cholesterol",
    "high density lipoprotein": "hdl_cholesterol",
    "high-density lipoprotein cholesterol": "hdl_cholesterol",
    
    # LDL
    "ldl": "ldl_cholesterol",
    "ldl cholesterol": "ldl_cholesterol",
    "ldl-cholesterol": "ldl_cholesterol",
    "ldl-c": "ldl_cholesterol",
    "low density lipoprotein": "ldl_cholesterol",
    "low-density lipoprotein cholesterol": "ldl_cholesterol",
    
    # Triglycerides
    "triglycerides": "triglycerides",
    "triglyceride": "triglycerides",
    "tg": "triglycerides",
    "serum triglycerides": "triglycerides",
    
    # VLDL
    "vldl": "vldl_cholesterol",
    "vldl cholesterol": "vldl_cholesterol",
    "vldl-c": "vldl_cholesterol",
    "very low density lipoprotein": "vldl_cholesterol",
    
    # Vitamin D
    "vitamin d": "vitamin_d",
    "vitamin d3": "vitamin_d",
    "vit d": "vitamin_d",
    "vit-d": "vitamin_d",
    "25-hydroxy vitamin d": "vitamin_d",
    "25-oh vitamin d": "vitamin_d",
    "vitamin d (25-oh)": "vitamin_d",
    "25-hydroxycholecalciferol": "vitamin_d",
    
    # Creatinine
    "creatinine": "creatinine",
    "serum creatinine": "creatinine",
    "creat": "creatinine",
    "creatinine serum": "creatinine",
    
    # BUN
    "bun": "blood_urea_nitrogen",
    "blood urea nitrogen": "blood_urea_nitrogen",
    "urea nitrogen": "blood_urea_nitrogen",
    "serum urea": "blood_urea_nitrogen",
    "urea": "blood_urea_nitrogen",
    
    # WBC
    "wbc": "wbc",
    "total wbc count": "wbc",
    "white blood cells": "wbc",
    "white blood cell count": "wbc",
    "total leukocyte count": "wbc",
    "total leucocyte count": "wbc",
    "tlc": "wbc",
    "leukocytes": "wbc",
    
    # RBC
    "rbc": "rbc",
    "red blood cells": "rbc",
    "red blood cell count": "rbc",
    "total rbc count": "rbc",
    "erythrocytes": "rbc",
    
    # Platelets
    "platelets": "platelets",
    "platelet count": "platelets",
    "plt": "platelets",
    "total platelet count": "platelets",
    "thrombocytes": "platelets",
    
    # Hematocrit / PCV
    "pcv": "hematocrit",
    "packed cell volume": "hematocrit",
    "hematocrit": "hematocrit",
    "haematocrit": "hematocrit",
    "hct": "hematocrit",
    
    # MCV, MCH, MCHC
    "mcv": "mcv",
    "mean corpuscular volume": "mcv",
    "mch": "mch",
    "mean corpuscular hemoglobin": "mch",
    "mean corpuscular haemoglobin": "mch",
    "mchc": "mchc",
    "mean corpuscular hemoglobin concentration": "mchc",
    
    # HbA1c
    "hba1c": "hba1c",
    "glycated hemoglobin": "hba1c",
    "glycosylated hemoglobin": "hba1c",
    "glycohemoglobin": "hba1c",
    "a1c": "hba1c",
    
    # Liver enzymes
    "alt": "alt",
    "sgpt": "alt",
    "alanine transaminase": "alt",
    "alanine aminotransferase": "alt",
    "ast": "ast",
    "sgot": "ast",
    "aspartate transaminase": "ast",
    "aspartate aminotransferase": "ast",
    "total bilirubin": "bilirubin_total",
    "bilirubin total": "bilirubin_total",
    "serum bilirubin": "bilirubin_total",
    "albumin": "albumin",
    "serum albumin": "albumin",
    "total protein": "total_protein",
    "serum protein": "total_protein",
    
    # Others
    "tsh": "tsh",
    "thyroid stimulating hormone": "tsh",
    "calcium": "calcium",
    "serum calcium": "calcium",
    "potassium": "potassium",
    "serum potassium": "potassium",
    "sodium": "sodium",
    "serum sodium": "sodium"
}

def clean_biomarker_text(raw_name: str) -> str:
    """Cleans punctuation, unwanted leading markers, and trims whitespace."""
    s = raw_name.strip()
    s = re.sub(r"^[\*\-\•\:\.\,\s]+", "", s)
    s = re.sub(r"[\*\:\.\,\s]+$", "", s)
    # Collapse multiple spaces
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def normalize_biomarker_name(raw_name: str) -> Tuple[str, str, str]:
    """
    Normalizes a biomarker name.
    Returns: (normalized_key, display_name, category)
    If no alias is confidently matched: preserves cleaned original name safely.
    """
    cleaned = clean_biomarker_text(raw_name)
    lookup_key = cleaned.lower()
    
    # Strip common prefixes like 'serum ', 'blood ', 'total ' if not matched initially
    if lookup_key in BIOMARKER_ALIASES:
        canonical_key = BIOMARKER_ALIASES[lookup_key]
        reg_info = BIOMARKER_CANONICAL_REGISTRY.get(canonical_key, {})
        display_name = reg_info.get("displayName", cleaned.title())
        category = reg_info.get("category", "General")
        return canonical_key, display_name, category

    # Try secondary cleaning (remove parenthetical content like '(serum)')
    simplified = re.sub(r"\([^)]*\)", "", lookup_key).strip()
    if simplified in BIOMARKER_ALIASES:
        canonical_key = BIOMARKER_ALIASES[simplified]
        reg_info = BIOMARKER_CANONICAL_REGISTRY.get(canonical_key, {})
        display_name = reg_info.get("displayName", cleaned.title())
        category = reg_info.get("category", "General")
        return canonical_key, display_name, category

    # Safe fallback: create a safe slug key, title-cased display name, without guessing
    slug_key = re.sub(r"[^a-zA-Z0-9]+", "_", lookup_key).strip("_")
    if not slug_key:
        slug_key = "biomarker_unknown"
    return slug_key, cleaned.title(), "Other Tests"

def parse_reference_range(ref_str: Optional[str]) -> Tuple[Optional[float], Optional[float]]:
    """
    Parses a reference range string into (low, high) float bounds if available.
    Examples:
      '12.0 - 16.0' -> (12.0, 16.0)
      '12.0 - 16.0 g/dL' -> (12.0, 16.0)
      '< 200' -> (None, 200.0)
      '> 60' -> (60.0, None)
      '70-99' -> (70.0, 99.0)
    """
    if not ref_str:
        return None, None
    s = ref_str.strip()
    
    # Match standard range: 12.0 - 16.0 or 12.0 to 16.0
    range_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|–|to)\s*(\d+(?:\.\d+)?)", s)
    if range_match:
        try:
            return float(range_match.group(1)), float(range_match.group(2))
        except ValueError:
            pass

    # Match upper limit: < 200 or <= 200 or Up to 200
    upper_match = re.search(r"(?:<|<=|less than|up to)\s*(\d+(?:\.\d+)?)", s, re.IGNORECASE)
    if upper_match:
        try:
            return None, float(upper_match.group(1))
        except ValueError:
            pass

    # Match lower limit: > 60 or >= 60 or Greater than 60
    lower_match = re.search(r"(?:>|>=|greater than)\s*(\d+(?:\.\d+)?)", s, re.IGNORECASE)
    if lower_match:
        try:
            return float(lower_match.group(1)), None
        except ValueError:
            pass

    return None, None

def determine_status(value: Optional[float], ref_low: Optional[float], ref_high: Optional[float]) -> str:
    """
    Determines status flag: 'normal', 'low', 'high', or 'unspecified'.
    Neutral categorization purely based on whether value falls within numeric interval.
    """
    if value is None:
        return "unspecified"
    if ref_low is not None and value < ref_low:
        return "low"
    if ref_high is not None and value > ref_high:
        return "high"
    if ref_low is not None or ref_high is not None:
        return "normal"
    return "unspecified"
