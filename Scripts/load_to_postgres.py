import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

csv_path = Path("data/processed/retail_prices_clean.csv")

if not csv_path.exists():
    raise FileNotFoundError("Cleaned CSV not found. Run transform_data.py first.")

df = pd.read_csv(csv_path)

df.insert(0, "id", range(1, len(df) + 1))

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)

engine = create_engine(connection_url)

with engine.begin() as connection:
    connection.execute(text("DROP TABLE IF EXISTS retail_prices;"))

    connection.execute(
        text("""
        CREATE TABLE retail_prices (
            id INTEGER PRIMARY KEY,
            date DATE NOT NULL,
            location TEXT NOT NULL,
            product TEXT NOT NULL,
            unit TEXT NOT NULL,
            price NUMERIC(10, 2) NOT NULL
        );
        """)
    )

df.to_sql(
    "retail_prices",
    engine,
    if_exists="append",
    index=False
)

print("Data loaded into PostgreSQL successfully.")
print(f"Rows loaded: {len(df)}")
print("Table created: retail_prices")