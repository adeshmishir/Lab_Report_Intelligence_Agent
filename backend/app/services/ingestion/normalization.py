"""Deterministic, explainable alias normalization for common lab test names.

The alias table is intentionally small. Only obvious, safe mappings are
included so the behavior stays auditable. The original wording is always
preserved on the result; normalization only affects ``test_name_normalized``.
"""

import re


def _key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


ALIASES = {
    "hba1c": "HbA1c",
    "hba1": "HbA1c",
    "a1c": "HbA1c",
    "hemoglobina1c": "HbA1c",
    "haemoglobina1c": "HbA1c",
    "glycatedhemoglobin": "HbA1c",
    "glycohemoglobin": "HbA1c",
    "hgb": "Hemoglobin",
    "hb": "Hemoglobin",
    "hg": "Hemoglobin",
    "hct": "Hematocrit",
    "rbc": "Red Blood Cells",
    "wbc": "White Blood Cells",
    "gran": "Granulocytes",
    "plts": "Platelets",
    "hdlc": "HDL",
    "hdlc": "HDL",
    "hdl-c": "HDL",
    "hdlcholesterol": "HDL",
    "ldlc": "LDL",
    "ldl-c": "LDL",
    "ldlcholesterol": "LDL",
    "vldlc": "VLDL",
    "vldl-c": "VLDL",
    "tg": "Triglycerides",
    "trig": "Triglycerides",
    "trl": "Triglycerides",
    "triglyceride": "Triglycerides",
    "creat": "Creatinine",
    "bun": "Blood Urea Nitrogen",
    "totchol": "Total Cholesterol",
    "chol": "Cholesterol",
}


def normalize_test_name(test_name: str) -> str:
    """Return the canonical name for a test, preserving the input otherwise."""
    name = (test_name or "").strip()
    if not name:
        return name
    return ALIASES.get(_key(name), name)


def normalize_unit(unit: str | None) -> str | None:
    if not unit or not unit.strip():
        return None
    key = re.sub(r"\s+", "", unit).lower()
    return {
        "mg/dl": "mg/dL",
        "mgdl": "mg/dL",
        "g/dl": "g/dL",
        "gdl": "g/dL",
        "mmol/l": "mmol/L",
        "mmoll": "mmol/L",
    }.get(key, unit.strip())