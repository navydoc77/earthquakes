from lxml import html
import requests
from splinter import Browser
from selenium import webdriver
from flask import Flask, jsonify, render_template
from bs4 import BeautifulSoup as bs
import json

base_url = "https://api.weather.gov//alerts/active"
params = {
    "location": "coordinates",
    "effective": "effective",
    "expires": "expires",
    "status": "status",
    "severity": "severity",
    "urgency": "urgency",
    "event": "event",
    "senderName": "senderName",
    "headline": "headline",
    "response": "respose",
}
params['keyword'] = warning

warning = []
