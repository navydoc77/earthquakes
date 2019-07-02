# from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html", listings=listings)


# @app.route("/scrape")
# def scraper():
#     listings.update({}, listings_data, upsert=True)
#     return redirect("/", code=302)


# if __name__ == "__main__":
#     app.run(debug=True)
import requests
from splinter import Browser
from bs4 import BeautifulSoup

# get_ipython().system('which chromedriver')

data = requests.get('http://10.0.0.10:1234/scrape.html')

# load data into bs4
soup = BeautifulSoup(data.text, 'html.parser')

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://alerts.weather.gov/cap/us.php?x=1'
browser.visit(url)

for tbody in soup.find_all("table"):
    values = [tbody.text for tbody in tbody.find_all('table')]
    print(values)