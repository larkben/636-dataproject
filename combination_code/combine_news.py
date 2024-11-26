import os
import csv

# Define input folder (containing .txt files) and output .csv file
input_folder = "/workspaces/636-dataproject/news"  # Update to the folder containing your .txt files
output_file = "/workspaces/636-dataproject/data/combine.csv"

# Function to process a single .txt file
def process_txt_file(file_path, company_name):
    articles = []  # List to store articles for the company
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Separate articles by empty lines or a clear pattern
        entries = content.strip().split('\n\n')  # Adjust as necessary if articles have different delimiters
        for entry in entries:
            lines = entry.split('\n')  # Split each article into lines
            if len(lines) >= 4:  # Ensure we have at least Title, Published, Source, and Summary
                title = lines[0].strip()
                published = "Unknown"
                source = "Unknown"
                summary = "Unknown"
                # Extract Published and Source from the following lines
                for line in lines[1:]:
                    if "Published:" in line:
                        published = line.split("Published:")[1].strip()
                    elif "Source:" in line:
                        source = line.split("Source:")[1].strip()
                    else:
                        summary = summary + " " + line.strip() if summary != "Unknown" else line.strip()
                # Append the processed article to the list
                articles.append([company_name, title, published, source, summary])
    return articles

# Process all .txt files in the folder
all_articles = []
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        company_name = filename.replace(".txt", "")  # Use the filename (without .txt) as the company name
        file_path = os.path.join(input_folder, filename)
        all_articles.extend(process_txt_file(file_path, company_name))

# Write all processed articles to a .csv file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header
    writer.writerow(["Company", "Title", "Published", "Source", "Summary"])
    # Write the data rows
    writer.writerows(all_articles)

print(f"Data has been successfully saved to {output_file}")
