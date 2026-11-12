import pandas as pd
from pathlib import Path


# ==========================================
# 1. PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 2. DATA EXTRACTION
# ==========================================

orders = pd.read_csv(
    PROCESSED_DIR / "olist_orders_dataset_cleaned.csv"
)

customers = pd.read_csv(
    PROCESSED_DIR / "olist_customers_dataset_cleaned.csv"
)


# ==========================================
# 3. DATA INTEGRATION
# ==========================================

ORDERS = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="one_to_one"
)


# ==========================================
# 4. COLUMN SELECTION
# ==========================================

selected_columns = [
    "order_id",
    "customer_id",
    "customer_zip_code_prefix",
    "customer_state",
    "order_approved_at",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

ORDERS = ORDERS[selected_columns]


# ==========================================
# 5. DATA EXPORT
# ==========================================

output_path = PROCESSED_DIR / "ORDERS.csv"

ORDERS.to_csv(
    output_path,
    index=False,
    encoding="utf-8"
)


# ==========================================
# 6. VERIFICATION
# ==========================================

print("Orders + Customers integration completed!")

print(f"Number of rows: {len(ORDERS)}")
print(f"Number of columns: {len(ORDERS.columns)}")

print("\nColumns:")
print(ORDERS.columns.tolist())

print("\nMissing values:")
print(ORDERS.isnull().sum())

print("\nUnique order_id:")
print(ORDERS["order_id"].is_unique)

print(f"\nFile saved successfully: {output_path}")
