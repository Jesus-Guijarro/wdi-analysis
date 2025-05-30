#!/usr/bin/env python3
import os
import requests
import zipfile
import io

# 1. Path configuration
DATA_DIR = "data"
ZIP_URL = "https://databank.worldbank.org/data/download/WDI_CSV.zip"

os.makedirs(DATA_DIR, exist_ok=True)

# 2. Download the ZIP archive
print("Downloading WDI_CSV.zip")
response = requests.get(ZIP_URL, stream=True)
response.raise_for_status()
zip_file = zipfile.ZipFile(io.BytesIO(response.content))

# 3. Extract only the CSVs we need and ignore the rest
print("Extracting required files")
for member in zip_file.namelist():
    basename = os.path.basename(member)
    if basename in ("WDICountry.csv", "WDISeries.csv", "WDICSV.csv"):
        zip_file.extract(member, DATA_DIR)

# 4. Transform the CSV files (remove all newline chars)
def transform_csv(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8', newline='') as f_in:
        data = f_in.read().replace('\n', '')
    with open(output_path, 'w', encoding='utf-8', newline='') as f_out:
        f_out.write(data)

print("Transforming WDICountry.csv → Countries.csv")
transform_csv(
    os.path.join(DATA_DIR, "WDICountry.csv"),
    os.path.join(DATA_DIR, "Countries.csv")
)

print("Transforming WDISeries.csv → Indicators.csv")
transform_csv(
    os.path.join(DATA_DIR, "WDISeries.csv"),
    os.path.join(DATA_DIR, "Indicators.csv")
)
# Remove raw intermediate CSVs
for raw in ("WDICountry.csv", "WDISeries.csv"):
    raw_path = os.path.join(DATA_DIR, raw)
    if os.path.exists(raw_path):
        os.remove(raw_path)

# 5. Rename Data CSV and cleanup raw files
print("Renaming WDICSV.csv → Data.csv")
os.rename(
    os.path.join(DATA_DIR, "WDICSV.csv"),
    os.path.join(DATA_DIR, "Data.csv")
)

print("Done")
