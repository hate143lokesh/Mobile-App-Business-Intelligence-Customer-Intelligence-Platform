
import pandas as pd
from pathlib import Path

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load processed dataset
file_path = BASE_DIR / "data" / "processed" / "Ecommerce_cleaned.csv"

df = pd.read_csv(file_path)

# Features expected by our ML model
features = [
    "device_type",
    "user_type",
    "marketing_channel",
    "product_id",
    "product_category",
    "unit_price",
    "quantity",
    "discount_percent",
    "pages_viewed",
    "time_on_site_sec",
    "added_to_cart",
    "visit_day",
    "visit_month",
    "visit_weekday",
    "visit_season",
    "session_duration_bucket",
    "location"
]

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

print("\n--- FEATURE DATA TYPES ---")
print(df[features].dtypes)

print("\n--- ALL FEATURE UNIQUE VALUES ---")

for col in features:
    values = sorted(df[col].dropna().unique().tolist())
    print(f"{col}: {values[:20]}")

print("\n--- MISSING VALUES ---")
print(df[features].isnull().sum())

print("\n--- NUMERIC FEATURE RANGES ---")
print(df[features].describe().round(2))



print("\n--- FEATURE DATA TYPES ---")
print(df[features].dtypes)

print("\n--- ALL FEATURE UNIQUE VALUES ---")
for col in features:
    print(f"{col}: {sorted(df[col].dropna().unique().tolist())[:30]}")
