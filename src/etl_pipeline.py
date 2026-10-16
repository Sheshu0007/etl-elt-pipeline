
import pandas as pd
from pathlib import Path
from datetime import datetime

# File paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "orders_raw.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
AUDIT_FILE = OUTPUT_DIR / "audit_log.csv"

# Extract data with error handling
try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    print(f"Error: Input file not found: {INPUT_FILE}")
    raise SystemExit(1)

print("Rows extracted:", len(df))

# Validate required columns
required_columns = [
    "order_id", "customer_id", "customer_name", "email",
    "city", "order_date", "product", "quantity",
    "unit_price", "updated_at"
]

if not all(col in df.columns for col in required_columns):
    raise ValueError("Required columns are missing")

# Clean text fields
for col in ["customer_name", "email", "city", "product"]:
    df[col] = df[col].astype("string").str.strip()
    df[col] = df[col].replace("", pd.NA)

# Convert numeric columns
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

# Identify invalid records
invalid = (
    df[required_columns].isna().any(axis=1)
    | df["order_id"].duplicated(keep=False)
    | (df["quantity"] <= 0)
    | (df["unit_price"] < 0)
    | ~df["email"].str.contains("@", na=False)
)

# Separate valid and rejected records
rejected = df[invalid].copy()
clean = df[~invalid].copy()

# Add rejection reason
rejected["rejection_reason"] = (
    "Missing value, duplicate ID, or invalid data"
)

# Calculate total sales
clean["total_amount"] = clean["quantity"] * clean["unit_price"]

# Save output files
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
clean.to_csv(OUTPUT_DIR / "orders_clean.csv", index=False)
rejected.to_csv(OUTPUT_DIR / "orders_rejected.csv", index=False)

# Display results
total_sales = clean["total_amount"].sum()

print("Valid rows:", len(clean))
print("Rejected rows:", len(rejected))
print("Total sales:", total_sales)
print("ETL completed successfully")

# Save audit log
audit = {
    "run_time": datetime.now().isoformat(timespec="seconds"),
    "rows_extracted": len(df),
    "rows_valid": len(clean),
    "rows_rejected": len(rejected),
    "total_sales": total_sales,
    "status": "SUCCESS"
}

audit_df = pd.DataFrame([audit])

audit_df.to_csv(
    AUDIT_FILE,
    mode="a",
    header=not AUDIT_FILE.exists(),
    index=False
)

print("Audit log saved.")
