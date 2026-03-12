import pandas as pd
import os

data_path = "data"

files = [
    "orders.csv",
    "order_items.csv",
    "products.csv",
    "website_sessions.csv",
    "website_pageviews.csv",
    "order_item_refunds.csv",
    "customer_360.csv",
    "datetable.csv"
]

for file in files:
    df = pd.read_csv(os.path.join(data_path, file))
    parquet_name = file.replace(".csv", ".parquet")
    df.to_parquet(os.path.join(data_path, parquet_name))
    print(f"Converted {file} -> {parquet_name}")