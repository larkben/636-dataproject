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

# Function to process a single file
def process_file(file_path, company_name):
    articles = []
    skipped_local = []  # Track skipped entries
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        entries = content.split("•\n") if "•" in content else re.split(r'(?<=\n)"', content.strip())

        for entry in entries:
            lines = entry.strip().split("\n")
            if len(lines) > 1:
                title = None
                summary_lines = []
                stock_change = None
                published = "Unknown"
                source = "Unknown"

                for line in lines:
                    line = line.strip()
                    # Identify the title (first line that doesn't match a date or stock change)
                    if title is None and not re.search(r"days ago", line) and not re.search(r"[-+]\d+\.\d+%", line):
                        title = line
                    elif re.search(r"days ago", line):  # Identify relative date
                        days_ago_match = re.search(r"(\d+)\s+days ago", line)
                        if days_ago_match:
                            published = infer_published_date(days_ago_match.group(1))
                    elif re.search(r"[-+]\d+\.\d+%", line):  # Identify stock change
                        stock_change = line
                    elif any(keyword in line for keyword in ["StockStory", "Zacks", "Insider Monkey", "GlobeNewswire", "Simply Wall St."]):
                        source = line
                    else:
                        summary_lines.append(line)

                # Combine summary lines into one string
                summary = " ".join(summary_lines).strip()

                # Append the article to the list if valid
                if title and summary:
                    articles.append([company_name, title, published, source, summary, stock_change])
                else:
                    skipped_local.append(entry)  # Track skipped entries
            else:
                skipped_local.append(entry)

    # Log skipped entries for debugging
    if skipped_local:
        print(f"{len(skipped_local)} entries skipped in {file_path}")
        skipped_entries.extend(skipped_local)

    return articles

# Process all .txt files in the input folder
all_articles = []
skipped_entries = []  # Track skipped entries

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        company_name = filename.replace(".txt", "")
        file_path = os.path.join(input_folder, filename)
        all_articles.extend(process_file(file_path, company_name))

# Write processed data to CSV
output_headers = ["Company", "Title", "Published", "Source", "Summary", "Stock Change"]

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(output_headers)  # Write header
    writer.writerows(all_articles)  # Write rows

# Debugging for skipped entries
if skipped_entries:
    skipped_file = "/workspaces/636-dataproject/data/skipped_entries.txt"
    with open(skipped_file, 'w', encoding='utf-8') as f:
        for entry in skipped_entries:
            f.write(entry + "\n")
    print(f"Skipped entries saved to {skipped_file}")

print(f"Data successfully saved to {output_file}.")
