"""Clean the UCI Student Performance (Portuguese course) dataset.

Source: Cortez & Silva (2008), UCI Machine Learning Repository, CC BY 4.0.
Run from the project root:  python src/data_preprocessing.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "student-por.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "student_por_clean.csv"

DROP_COLUMNS = ["romantic"]  # private information, not justified for grade prediction

RENAME_MAP = {
    "Medu": "mother_edu", "Fedu": "father_edu",
    "Mjob": "mother_job", "Fjob": "father_job",
    "studytime": "study_time", "traveltime": "travel_time",
    "famrel": "family_relationship", "goout": "go_out",
    "Dalc": "alcohol_weekday", "Walc": "alcohol_weekend",
    "schoolsup": "school_support", "famsup": "family_support",
    "paid": "paid_classes", "higher": "wants_higher_ed",
    "G1": "g1", "G2": "g2", "G3": "g3",
}


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    """Load the raw semicolon-separated file."""
    return pd.read_csv(path, sep=";")


def validate(df: pd.DataFrame) -> None:
    """Stop with an error if the data breaks basic expectations."""
    assert df.isnull().sum().sum() == 0, "Missing values found"
    assert df.duplicated().sum() == 0, "Duplicate rows found"
    for col in ["g1", "g2", "g3"]:
        assert df[col].between(0, 20).all(), f"{col} outside 0-20"
    assert df["age"].between(15, 22).all(), "age outside 15-22"


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy; the input is never modified."""
    clean = df.copy().drop_duplicates()
    text_cols = clean.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        clean[col] = clean[col].str.strip()
    clean = clean.drop(columns=DROP_COLUMNS).rename(columns=RENAME_MAP)
    validate(clean)
    return clean


def main() -> None:
    raw = load_raw()
    clean = clean_data(raw)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(PROCESSED_PATH, index=False)
    print(f"Raw shape:   {raw.shape}")
    print(f"Clean shape: {clean.shape}")
    print(f"Saved to:    {PROCESSED_PATH}")


if __name__ == "__main__":
    main()