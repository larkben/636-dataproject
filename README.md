# 636-dataproject
The project for 636 involving analyzing sentiment and financial indicators from both Wallstreet and Retail to predict option future.

# directory

.venv is the packages being used with python
requirements.txt is the packages install script

# editing the package list

`pip freeze` only works once in the python enviroment; fetches all packages and adds them to requirements.txt

# scrapers
Reddit: https://github.com/JosephLai241/URS ~ look for easier or better options should they exist
Twitter: https://github.com/taspinar/twitterscraper
Google Scraper For Sentiment Analysis: https://github.com/gyanesh-m/Sentiment-analysis-of-financial-news-data

# setup

All OS:
- must have python 3 or higher installed

Mac OSX / Linux:
`python -m venv .venv; source ./.venv/bin/activate; pip install --upgrade pip; pip install -r requirements.txt`

Windows:
`write script here`

# clean up

Mac OSX / Linux (if in enviroment)
`deactivate; rm -rf .venv` removes the packages folder from directory
else:
`rm -rf .venv`

Windows
`write script here`
