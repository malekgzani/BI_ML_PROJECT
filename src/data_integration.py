
import pandas as pd
from pathlib import Path


# ==========================================
# 1. PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "processed"



# ==========================================
# 3. HELPER FUNCTION
# ==========================================

# Returns the most frequent non-null value.
# Useful for categorical aggregation.

def get_mode(series):

    mode = series.mode()

    if not mode.empty:
        return mode.iloc[0]

    return pd.NA


# ==========================================
# 4. ORDERS + CUSTOMERS
# ==========================================
orders = pd.read_csv(PROCESSED_DIR / "olist_orders_dataset_cleaned.csv")
customers = pd.read_csv(PROCESSED_DIR / "olist_customers_dataset_cleaned.csv")


ORDERS = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="one_to_one"
)

selected_columns = [
    "order_id",
    "customer_id",
    "customer_zip_code_prefix",
    "customer_state",
    "order_approved_at",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

ORDERS = ORDERS[selected_columns].copy()


# ==========================================
# 5. AGG PRODUCT
# ==========================================

# 5.1 Merge ORDER_ITEMS + PRODUCTS

order_items = pd.read_csv(PROCESSED_DIR / "olist_order_items_dataset_cleaned.csv")
products = pd.read_csv(PROCESSED_DIR / "olist_products_dataset_cleaned.csv")

product_details = order_items.merge(
    products,
    on="product_id",
    how="left",
    validate="many_to_one"
)


# 5.2 Aggregate products by ORDER_ID

AGG_PRODUCT = product_details.groupby("order_id").agg(

    nb_products=("order_item_id", "count"),

    nb_distinct_products=("product_id", "nunique"),

    nb_categories=("product_category_name", "nunique"),

    main_category=("product_category_name", get_mode),

    product_description_length_mean=(
        "product_description_lenght", "mean"
    ),

    product_photos_qty_mean=(
        "product_photos_qty", "mean"
    )

).reset_index()


# ==========================================
# 6. AGG SELLER
# ==========================================
sellers = pd.read_csv(PROCESSED_DIR / "olist_sellers_dataset_cleaned.csv")
closed_deals = pd.read_csv(PROCESSED_DIR / "olist_closed_deals_dataset_cleaned.csv")

# 6.1 Aggregate CLOSED DEALS by SELLER_ID
# This avoids duplicating sellers during the merge.

CLOSED_DEALS_AGG = closed_deals.groupby("seller_id").agg(

    business_segment=("business_segment", get_mode),

    lead_behaviour_profile=("lead_behaviour_profile", get_mode),

    business_type=("business_type", get_mode)

).reset_index()


# 6.2 Merge SELLERS + CLOSED DEALS
# LEFT JOIN keeps ALL sellers,
# including sellers without closed deals.

SELLER_DETAILS = sellers.merge(
    CLOSED_DEALS_AGG,
    on="seller_id",
    how="left",
    validate="one_to_one"
)


# 6.3 Add an indicator for closed deals

SELLER_DETAILS["has_closed_deal"] = (
    SELLER_DETAILS["business_segment"].notna()
).astype(int)


# 6.4 Merge ORDER_ITEMS + SELLER_DETAILS

seller_details = order_items.merge(
    SELLER_DETAILS,
    on="seller_id",
    how="left",
    validate="many_to_one"
)


# 6.5 Aggregate sellers by ORDER_ID

AGG_SELLER = seller_details.groupby("order_id").agg(

    nb_sellers=("seller_id", "nunique"),

    seller_state=("seller_state", get_mode),

    seller_city=("seller_city", get_mode),

    business_segment=("business_segment", get_mode),

    lead_behaviour_profile=("lead_behaviour_profile", get_mode),

    business_type=("business_type", get_mode),

    has_closed_deal=("has_closed_deal", "max")

).reset_index()


# ==========================================
# 7. AGG PAYMENT
# ==========================================
payments = pd.read_csv(PROCESSED_DIR / "olist_order_payments_dataset_cleaned.csv")

AGG_PAYMENT = payments.groupby("order_id").agg(

    total_payment_value=("payment_value", "sum"),

    payment_type_mode=("payment_type", get_mode),

    max_installments=("payment_installments", "max"),

    nb_payment_types=("payment_type", "nunique"),

    nb_payments=("payment_value", "count")

).reset_index()


# ==========================================
# 8. AGG REVIEW + TARGET
# ==========================================

# Define a negative review as a score <= 2.

reviews["negative_review"] = (
    reviews["review_score"] <= 2
).astype(int)


# Aggregate reviews by ORDER_ID.
# If multiple reviews exist, the order is negative
# if at least one review has a score <= 2.
reviews = pd.read_csv(PROCESSED_DIR / "olist_order_reviews_dataset_cleaned.csv")

AGG_REVIEW = reviews.groupby("order_id").agg(

    review_score_mean=("review_score", "mean"),

    negative_review=("negative_review", "max")

).reset_index()


# ==========================================
# 9. FINAL DATA INTEGRATION
# ==========================================

FINAL_DATASET = ORDERS.merge(
    AGG_PRODUCT,
    on="order_id",
    how="left",
    validate="one_to_one"
)

FINAL_DATASET = FINAL_DATASET.merge(
    AGG_SELLER,
    on="order_id",
    how="left",
    validate="one_to_one"
)

FINAL_DATASET = FINAL_DATASET.merge(
    AGG_PAYMENT,
    on="order_id",
    how="left",
    validate="one_to_one"
)

FINAL_DATASET = FINAL_DATASET.merge(
    AGG_REVIEW,
    on="order_id",
    how="left",
    validate="one_to_one"
)


# ==========================================
# 10. REMOVE DATA LEAKAGE
# ==========================================

# review_score is used to construct the target.
# It must not be used as a model feature.

FINAL_DATASET = FINAL_DATASET.drop(
    columns=["review_score_mean"]
)


# ==========================================
# 11. DATA EXPORT
# ==========================================

AGG_PRODUCT.to_csv(
    PROCESSED_DIR / "AGG_PRODUCT.csv",
    index=False,
    encoding="utf-8"
)

AGG_SELLER.to_csv(
    PROCESSED_DIR / "AGG_SELLER.csv",
    index=False,
    encoding="utf-8"
)

AGG_PAYMENT.to_csv(
    PROCESSED_DIR / "AGG_PAYMENT.csv",
    index=False,
    encoding="utf-8"
)

AGG_REVIEW.to_csv(
    PROCESSED_DIR / "AGG_REVIEW.csv",
    index=False,
    encoding="utf-8"
)

FINAL_DATASET.to_csv(
    PROCESSED_DIR / "FINAL_DATASET.csv",
    index=False,
    encoding="utf-8"
)


# ==========================================
# 12. VERIFICATION
# ==========================================

print("\n========== INTEGRATION COMPLETED ==========")

print("\nORDERS:", ORDERS.shape)
print("AGG_PRODUCT:", AGG_PRODUCT.shape)
print("AGG_SELLER:", AGG_SELLER.shape)
print("AGG_PAYMENT:", AGG_PAYMENT.shape)
print("AGG_REVIEW:", AGG_REVIEW.shape)

print("\nFINAL DATASET")
print("Rows:", len(FINAL_DATASET))
print("Columns:", len(FINAL_DATASET.columns))

print("\nUnique order_id:")
print(FINAL_DATASET["order_id"].is_unique)

print("\nMissing values:")
print(FINAL_DATASET.isnull().sum())

print("\nTarget distribution:")
print(FINAL_DATASET["negative_review"].value_counts(dropna=False))

print("\nFinal columns:")
print(FINAL_DATASET.columns.tolist())

print("\nFile saved successfully:")
print(PROCESSED_DIR / "FINAL_DATASET.csv")
