import os
import csv
import re

# Define input folder and output .csv file paths
input_folder = "/workspaces/636-dataproject/news"  # Path to the folder containing your .txt files
output_file = "/workspaces/636-dataproject/data/combine.csv"  # Path for the output CSV file

# Function to process a single .txt file
def process_txt_file(file_path, company_name):
    articles = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Use regex to split articles starting with a quoted title
        entries = re.split(r'(?<=")\n', content.strip())  # Splits based on the end of a title line
        for entry in entries:
            lines = entry.split('\n')
            if len(lines) >= 3:  # Ensure there's enough content
                # Extract title (first line)
                title = lines[0].strip()
                published = "Unknown"
                source = "Unknown"
                summary = []

                # Extract Published, Source, and remaining content
                for line in lines[1:]:
                    if "Published:" in line:
                        published = line.split("Published:")[1].strip()
                    elif "Source:" in line:
                        source = line.split("Source:")[1].strip()
                    else:
                        summary.append(line.strip())

                # Combine the summary into a single string
                summary = " ".join(summary)
                # Append the structured article to the list
                articles.append([company_name, title, published, source, summary])
    return articles

# Process all .txt files in the input folder
all_articles = []
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        company_name = filename.replace(".txt", "")  # Use the filename (without .txt) as the company name
        file_path = os.path.join(input_folder, filename)
        all_articles.extend(process_txt_file(file_path, company_name))

# Write processed articles to a .csv file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header
    writer.writerow(["Company", "Title", "Published", "Source", "Summary"])
    # Write the rows
    writer.writerows(all_articles)

print(f"Data has been successfully saved to {output_file}")
