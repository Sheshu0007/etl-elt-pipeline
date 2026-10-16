
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "orders_raw.csv"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "orders_clean.csv"

# Required columns
REQUIRED_COLUMNS = [
    "order_id", "customer_id", "customer_name", "email", "city",
    "order_date", "product", "quantity", "unit_price", "updated_at"
]


def run_pipeline():
    # EXTRACT
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)
    print(f"Extracted {len(df)} rows.")

    # VALIDATE: Check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    # TRANSFORM: Clean text fields
    text_columns = [
        "customer_id", "customer_name", "email", "city", "product"
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # TRANSFORM: Convert numeric and date fields
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce")

    # VALIDATE: Check missing values
    if df[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError("Validation failed: missing or invalid values.")

    # VALIDATE: Check duplicate order IDs
    if df["order_id"].duplicated().any():
        raise ValueError("Validation failed: duplicate order IDs.")

    # VALIDATE: Check business rules
    if (df["quantity"] <= 0).any():
        raise ValueError("Quantity must be greater than zero.")

    if (df["unit_price"] < 0).any():
        raise ValueError("Unit price cannot be negative.")

    if not df["email"].str.contains("@", regex=False).all():
        raise ValueError("Invalid email detected.")

    # TRANSFORM: Calculate order totals
    df["total_amount"] = df["quantity"] * df["unit_price"]

    # LOAD: Save clean output separately
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Validation passed: {len(df)} rows.")
    print(f"Output saved to: {OUTPUT_FILE}")
    print(f"Total sales: {df['total_amount'].sum():,.2f}")


if __name__ == "__main__":
    run_pipeline()
