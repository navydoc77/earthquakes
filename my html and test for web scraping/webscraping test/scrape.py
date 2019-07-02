from lxml import html
import requests
from splinter import Browser
from selenium import webdriver
from flask import Flask, jsonify, render_template
from bs4 import BeautifulSoup as bs
# import MySQLdb

# HOST = "localhost"
# USERNAME = "root"
# PASSWORD = "root"
# DATABASE = "scraping"

page = requests.get('https://kamala.cod.edu/svr/')
tree = html.fromstring(page.content)

storm = tree.xpath('//font["SVR T-STORM WARNING"]/text()')
flood = tree.xpath('//font["FLASH FLOOD WARNING"]/text()')
tornado = tree.xpath('//font["TORNADO WARNING"]/text()')


print('SVR T-STORM WARNING:', storm)
print('FLASH FLOOD WARNING:', flood)
print('TORNADO WARNING:', tornado)

# storms: []
floods: []
tornados: []

app = Flask(__name__, template_folder = "templates")

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

# @app.route("storms")
# def storms():
#     storms = [storms]

#     return jsonify(list(storms))

if __name__ == '__main__':
    app.run(debug=True)

# def init_browser():
#     executable_path = {}
#     return Browser("chrome", **executable_path, headless=False)

# def scrape():
#     page = requests.get('https://kamala.cod.edu/svr/')
#     tree = html.fromstring(page.content)

#     storm = tree.xpath('//font["SVR T-STORM WARNING"]/text()')
#     flood = tree.xpath('//font["FLASH FLOOD WARNING"]/text()')
#     tornado = tree.xpath('//font["TORNADO WARNING"]/text()')

#     print('SVR T-STORM WARNING:', storm)
#     print('FLASH FLOOD WARNING:', flood)
#     print('TORNADO WARNING:', tornado)

#     storm: []
#     flood: []
#     tornado: []

# app = Flask(__name__)

# @app.route("/")
# def index():
#     """Return the homepage."""
#     return render_template("index.html")

# if __name__ == "__main__":
#     print(scrape())

