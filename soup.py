
from webbrowser import Error

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests
import re
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait

def get_info(query):

    # Fetch the search results page from Yahoo Finance
    search_url = f"https://www.alphaquery.com/stock/{query}/profile-key-metrics"
    print(search_url)
    soup = BeautifulSoup(requests.get(search_url).content, 'html.parser')

    html_list_financial = soup.find_all('div', class_="col-lg-6")
    html_list_stocks = soup.find('div', class_="col-lg-4 col-md-12 margin-top-rem")

    html_list = str(html_list_financial).split('\n')

    html_list_stock = str(html_list_stocks).split('\n')

    data_finance = []
    data_stock = []

    for index, html in enumerate(html_list):
        if html == "<tr>":
            data_finance.append((html_list[index+1],html_list[index+2]))

    for index, data in enumerate(html_list_stock):
        if data == "<tr>":
            data_stock.append((html_list_stock[index+1],html_list_stock[index+2]))


    return data_finance, data_stock

def get_ticker(company_name):

    # Replace spaces in the company name with '+' for the search query
    search_query = company_name.replace(" ", "+")

    # Fetch the search results page from Yahoo Finance
    search_url = f"https://finance.yahoo.com/lookup?s={search_query}"

    driver = webdriver.Edge()

    pattern = re.compile(re.escape(search_query), re.IGNORECASE)

    try:
        driver.get(search_url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a")))
        print(f"Query: {search_query}")
        print(f"Search URL: {search_url}")

        # Beautiful Soup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ticker_tags = soup.find('a', class_="loud-link fin-size-medium yf-1e4diqp")
        words = str(ticker_tags).split(' ')
        word = words[len(words)-2]
        ticker = ''
        for index, char in enumerate(word):
            if(char == '>'):
                ticker = word[index+1:]
                break
        return ticker
    except Error as e:
        return "Ticker not found"

if __name__ == '__main__':
    data_finance, data_stock = get_info(get_ticker('Reddit'))

    data_qual = []
    data_quan = []
    data_stk = []

    for data in data_finance:
        data_qual.append(data[0].split('<td>')[1].split('</td>')[0])
        data_quan.append(data[1].split('>')[1].split('<')[0])

    for data in data_stock:
        print(data[0], '\n', data[1])

    for data in data_stock:
        try:
            data_qual.append(data[0].split('<td>')[1].split('</td>')[0])
        except IndexError:
            data_qual.append("Qualitative data not found")
        if data[1][:9] == "td class=":
            data_quan.append(data[1].split('>')[1].split('<')[0])
        else:
            data_quan.append(data[1].split('<td>')[1].split('</td>')[0])

    print(data_stock)
    for i in range(len(data_qual)):
        print(data_qual[i], "\n", data_quan[i])
   # for result in results:
   #     print(result)

