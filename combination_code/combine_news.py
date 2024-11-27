import os
import csv
import re
from datetime import datetime, timedelta

# Define input folder and output file paths
input_folder = "/workspaces/636-dataproject/data/backupdata/news"
output_file = "/workspaces/636-dataproject/data/combine_news.csv"

# Function to infer published date based on "days ago"
def infer_published_date(relative_days):
    try:
        relative_days = int(relative_days)
        published_date = datetime.now() - timedelta(days=relative_days)
        return published_date.strftime('%B %d, %Y')
    except ValueError:
        return "Unknown"

# General function to process .txt files
def process_file(file_path, company_name):
    articles = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if "•" in content:  # Special structure for files like powl.txt
            entries = content.split("•\n")
            for entry in entries:
                lines = entry.strip().split("\n")
                if len(lines) > 1:
                    title = lines[0].strip()
                    published = "Unknown"
                    source = "Unknown"
                    summary_lines = []

                    for line in lines[1:]:
                        if re.search(r"days ago", line):
                            days_ago = re.search(r"(\d+)\s+days ago", line)
                            if days_ago:
                                published = infer_published_date(days_ago.group(1))
                        elif any(keyword in line for keyword in ["StockStory", "Zacks", "Insider Monkey", "GlobeNewswire", "Simply Wall St."]):
                            source = line.strip()
                        else:
                            summary_lines.append(line.strip())
                    
                    summary = " ".join(summary_lines).strip()
                    articles.append([company_name, title, published, source, summary])
                else:
                    print(f"Skipped entry in {file_path}: {entry}")  # Debug skipped entries
        else:  # Standard structure for most files
            entries = re.split(r'(?<=\n)"', content.strip())
            for entry in entries:
                lines = entry.split("\n")
                if len(lines) >= 3:
                    title = lines[0].strip().strip('"')
                    published = "Unknown"
                    source = "Unknown"
                    summary_lines = []

                    for line in lines[1:]:
                        if "Published:" in line:
                            published = line.split("Published:")[1].strip()
                        elif "Source:" in line:
                            source = line.split("Source:")[1].strip()
                        else:
                            summary_lines.append(line.strip())

                    summary = " ".join(summary_lines)
                    articles.append([company_name, title, published, source, summary])
                else:
                    print(f"Skipped entry in {file_path}: {entry}")
    return articles

# Process all .txt files in the input folder
all_articles = []
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        company_name = filename.replace(".txt", "")
        file_path = os.path.join(input_folder, filename)
        all_articles.extend(process_file(file_path, company_name))

# Write all processed articles to a .csv file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company", "Title", "Published", "Source", "Summary"])
    writer.writerows(all_articles)

print(f"Data has been successfully saved to {output_file}")
