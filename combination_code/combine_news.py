import os
import csv
import re

# Define input folder and output .csv file paths
input_folder = "./news"  # Folder where .txt files are stored
output_file = "./data/combine.csv"  # Path for the output CSV file

# Function to process a single .txt file
def process_txt_file(file_path, company_name):
    articles = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Use regex to split articles, assuming each article starts with a quoted title
        entries = re.split(r'(?<=\n)"', content.strip())  # Match articles starting with "
        for entry in entries:
            lines = entry.split('\n')
            if len(lines) >= 3:  # Ensure there's enough content
                title = lines[0].strip().strip('"')  # First line as Title
                published = "Unknown"
                source = "Unknown"
                summary_lines = []

                # Parse the rest of the lines for Published, Source, and Summary
                for line in lines[1:]:
                    if "Published:" in line:
                        published = line.split("Published:")[1].strip()
                    elif "Source:" in line:
                        source = line.split("Source:")[1].strip()
                    else:
                        summary_lines.append(line.strip())

                # Combine summary lines into a single string
                summary = " ".join(summary_lines)
                # Append article data as a row
                articles.append([company_name, title, published, source, summary])
    return articles

# Process all .txt files in the input folder
all_articles = []
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        company_name = filename.replace(".txt", "")  # Use the filename (without .txt) as company name
        file_path = os.path.join(input_folder, filename)
        all_articles.extend(process_txt_file(file_path, company_name))

# Write all processed articles to a .csv file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header
    writer.writerow(["Company", "Title", "Published", "Source", "Summary"])
    # Write the rows
    writer.writerows(all_articles)

print(f"Data has been successfully saved to {output_file}")
