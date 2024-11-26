import os
import pandas as pd

# Define the folder containing the .txt files and the output CSV file
input_folder = "/workspaces/636-dataproject/news"  # Replace with your actual folder path
output_csv = "/workspaces/636-dataproject/data/combined_news_data.csv"

# Initialize an empty list to hold the data
combined_data = []

# Iterate over all .txt files in the folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".txt"):  # Process only .txt files
        company_name = file_name.replace(".txt", "")  # Extract company name from the file name
        file_path = os.path.join(input_folder, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()  # Read the content of the file
            articles = content.strip().split("\n\n")  # Split articles by double line breaks

            # Process each article
            for article in articles:
                lines = article.strip().split("\n")
                if len(lines) >= 4:  # Ensure the article has all required lines
                    title = lines[0]
                    published = lines[1].replace("Published: ", "").strip()
                    source = lines[2].replace("Source: ", "").strip()
                    summary = lines[3].replace("Summary: ", "").strip()

                    # Append the data to the combined list
                    combined_data.append({
                        "Company": company_name,
                        "Title": title,
                        "Published": published,
                        "Source": source,
                        "Summary": summary
                    })

# Convert the combined data into a DataFrame
df = pd.DataFrame(combined_data)

# Save the DataFrame to a CSV file
df.to_csv(output_csv, index=False)

print(f"Combined news data saved to {output_csv}")
