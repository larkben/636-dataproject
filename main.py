from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_url(company, date_start=None, date_end=None):
    print()

if __name__ == '__main__':
    req = requests.get('https://x.com/DividendTalks/status/1850279953075675313')
    soup = BeautifulSoup(req.text, features='html.parser')
    print(soup.prettify())
