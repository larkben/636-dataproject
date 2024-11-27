from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import csv
import time

# Keywords to filter headlines
keywords = ["Palo Alto", "PANW"]  # Add your keywords here

# Path to your ChromeDriver (replace with the actual path to chromedriver)
CHROMEDRIVER_PATH = r'C:\Users\corey\OneDrive\Desktop\chromedriver-win64\chromedriver.exe'

# Set up the Selenium WebDriver with headless mode for efficiency
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to Yahoo Finance News page
    url = 'https://finance.yahoo.com/quote/PANW/news/'
    driver.get(url)

    # Scroll to load more content
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0

    while scroll_count < 1:  # Increase scroll count to load more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Increase delay to give the page more time to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Break if we've reached the end of the page
        if new_height == last_height:
            break
        last_height = new_height
        scroll_count += 1

    # Get the loaded page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Generate a CSV file name dynamically based on the keywords
    csv_filename = f'{keywords}.csv'

    # Find all headline elements
    articles = soup.find_all('li', class_='stream-item story-item yf-1usaaz9')
    print(f"Total headlines found after scrolling: {len(articles)}")  # Debugging: Check total count

    # Open a CSV file to save filtered headlines and dates
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Headline', 'Date'])  # Write header

        # Extract and write each headline and date
        for article in articles:
            headline_tag = article.find('h3')  # Adjust selector as needed
            date_tag = article.find('div', class_='publishing yf-1weyqlp')

            if headline_tag:
                title = headline_tag.get_text().strip()
                date = date_tag.get_text().strip()

                # Check for keywords in the headline
                if any(keyword.lower() in title.lower() for keyword in keywords):
                    writer.writerow([title, date])  # Write headline and date to CSV
                    print("Matching article:", title, "| Date:", date)  # Debugging output

    print(f"Filtered headlines have been saved to '{csv_filename}'")
finally:
    driver.quit()
