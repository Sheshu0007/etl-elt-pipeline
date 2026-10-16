
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CURRENT_FILE = BASE_DIR / "data" / "processed" / "orders_clean.csv"
NEW_FILE = BASE_DIR / "data" / "orders_test.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "orders_incremental.csv"

current = pd.read_csv(CURRENT_FILE)
new = pd.read_csv(NEW_FILE)

required = [
    "order_id", "customer_id", "customer_name", "email",
    "city", "order_date", "product", "quantity",
    "unit_price", "updated_at"
]

# Reject duplicate order IDs before any other filtering
duplicate_ids = new["order_id"].duplicated(keep=False)
new = new[~duplicate_ids].copy()

# Reject missing or empty required values
new = new.dropna(subset=required)
empty_rows = new[required].astype(str).apply(
    lambda col: col.str.strip().eq("")
).any(axis=1)
new = new[~empty_rows].copy()

# Validate numeric fields and email
new["quantity"] = pd.to_numeric(new["quantity"], errors="coerce")
new["unit_price"] = pd.to_numeric(new["unit_price"], errors="coerce")

new = new[
    new["email"].str.contains("@", na=False)
    & (new["quantity"] > 0)
    & (new["unit_price"] >= 0)
].copy()

# Exclude IDs already loaded
new = new[~new["order_id"].isin(current["order_id"])].copy()

new["total_amount"] = new["quantity"] * new["unit_price"]
result = pd.concat([current, new], ignore_index=True)

result.to_csv(OUTPUT_FILE, index=False)

print("Existing rows:", len(current))
print("Valid new rows:", len(new))
print("Final rows:", len(result))
print("Final order IDs:", result["order_id"].tolist())
