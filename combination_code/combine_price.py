import os
import pandas as pd

# Define the folder containing the .csv files
input_folder = "/workspaces/636-dataproject/data/backupdata/price_data"  # Replace with the path to your folder
output_file = "/workspaces/636-dataproject/data/combined_prices.csv"  # Path to save the combined CSV

# Initialize an empty list to hold dataframes
dataframes = []

# Initialize variables to calculate the total rows from individual files
total_rows_individual = 0

# Loop through all files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):  # Process only .csv files
        # Extract the company name from the filename
        company_name = filename.replace(".csv", "")
        file_path = os.path.join(input_folder, filename)
        
        # Read the .csv file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Add a new column for the company name
        df["Company"] = company_name
        
        # Append the DataFrame to the list
        dataframes.append(df)
        
        # Print the shape of the individual file
        print(f"File: {filename} - Shape: {df.shape}")
        
        # Update the total rows from individual files
        total_rows_individual += df.shape[0]

# Concatenate all the dataframes
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a new .csv file
combined_df.to_csv(output_file, index=False)

# Print the combined DataFrame shape
print(f"\nCombined Data Shape: {combined_df.shape}")

# Print the total rows from individual files
print(f"Total Rows from Individual Files: {total_rows_individual}")

# Verify the consistency
if total_rows_individual == combined_df.shape[0]:
    print("✅ The combined data rows match the sum of rows from individual files.")
else:
    print("❌ The combined data rows do NOT match the sum of rows from individual files.")
