from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import csv
import time

# Keywords to filter headlines
keywords = [""]  # Add your keywords here

# Path to your ChromeDriver (replace with the actual path to chromedriver)
CHROMEDRIVER_PATH = r'C:\Users\Corey\Desktop\Coding Projects\.vscode\chromedriver-win32\chromedriver.exe'

# Set up the Selenium WebDriver with headless mode for efficiency
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to Yahoo Finance Earnings page
    url = 'https://finance.yahoo.com/topic/earnings/'
    driver.get(url)

    # Scroll to load more content
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0

    while scroll_count < 20:  # Increase scroll count to load more content
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

    # Find all headline elements
    headlines = soup.find_all('h3', class_='clamp')
    print(f"Total headlines found after scrolling: {len(headlines)}")  # Debugging: Check total count

    # Open a CSV file to save filtered headlines
    with open('filtered_yahoo_finance_headlines.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Headline'])  # Write header

        # Write each headline that contains a keyword to the CSV
        for headline in headlines:
            title = headline.get_text().strip()
            if title and any(keyword.lower() in title.lower() for keyword in keywords):
                writer.writerow([title])
                print("Matching headline:", title)  # Print each matching headline to the console

    print("Filtered headlines have been saved to 'filtered_yahoo_finance_headlines.csv'")
finally:
    driver.quit()
