import pandas as pd
import requests

url = "https://www150.statcan.gc.ca/n1/tbl/csv/18100245-eng.zip"

output_path = "data/raw/canadian_retail_prices.zip"

response = requests.get(url)

with open(output_path, "wb") as file:
    file.write(response.content)

print("Canadian retail price data downloaded successfully.")