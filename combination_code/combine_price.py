import os
import pandas as pd

# Define file paths and corresponding company names
files_with_companies = {
    'price_intu.csv': 'intu',
    'price_keys.csv': 'keys',
    'price_nio.csv': 'nio',
    'price_nvda.csv': 'nvda',
    'price_panw.csv': 'panw',
    'price_powl.csv': 'powl',
    'price_snow.csv': 'snow',
    'price_sym.csv': 'sym',
    'price_tgt.csv': 'tgt',
    'price_wmt.csv': 'wmt'
}

# Path where uploaded files are stored
base_path = './price_data'

# Initialize an empty list to hold individual DataFrames
dfs = []

# Process each file
for file_name, company in files_with_companies.items():
    file_path = os.path.join(base_path, file_name)
    df = pd.read_csv(file_path)
    df['Company'] = company  # Add a column for the company name
    dfs.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined dataset to a new CSV file
output_path = './data/combined_prices.csv'
combined_df.to_csv(output_path, index=False)

output_path
