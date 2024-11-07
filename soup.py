from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

#uses selenium to get the information from twitter.
#A specific link is used with the %24 representing $ symbol for driver.get
#clasifications need to be changed to get valuable information (tweets = soup.find_all)
#soup.prettify shows us the pull is technically working
def get_info(query, date_start=None, date_end=None):
    
    driver = webdriver.Edge()
    driver.get(f'https://x.com/search?q=%24{query}&src=typed_query&f=top')
    # Wait for the page to load
    time.sleep(1) # Get the page source and parse it with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    print(soup.prettify())
    # Find the tweets (this will vary based on Twitter's HTML structure)
    tweets = soup.find_all('div', class_='tweet')
    # Extract and return the text from the tweets
    results = [tweet.get_text() for tweet in tweets] # Close the browser driver.quit()
    return results
#uses requests to get information from twitter
#classification needs to be changed
def get_url(query):

    url = f'https://x.com/search?q=%24{query}&src=typed_query&f=top'
    # Make a GET request to fetch the raw HTML content
    response = requests.get(url) # Parse the HTML content
    soup = BeautifulSoup(response.text, features="html.parser") 
    info = soup.find_all('div', class_='tweet') 
    # Extract and return the text from the found elements
    results = [element.get_text() for element in info]
    return results
if __name__ == '__main__':
    results = get_info('google')
    #results = get_url('google')
    for result in results:
        print(result)
