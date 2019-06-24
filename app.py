import os
from dotenv import load_dotenv

import pandas as pd
import numpy as np
from decimal import Decimal

# Dependencies for API call
import requests
import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

import pymysql
pymysql.install_as_MySQLdb()
import flask_sqlalchemy

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

#################################################
# Database & Flask Setup
#################################################

load_dotenv()

# Database Connection
dialect = os.getenv("DATABASE_DIALECT")
username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
port = os.getenv("DATABASE_PORT")
database = os.getenv("DATABASE_NAME")

# Format:
# `<Dialect>://<Username>:<Password>@<Host Address>:<Port>/<Database>`
# Using f-string notation: https://docs.python.org/3/reference/lexical_analysis.html#f-strings
# connection = f"{dialect}://{username}:{password}@{host}:{port}/{database}"
connection = f"{dialect}://{username}:{password}@{host}:{port}/{database}"

app.config["SQLALCHEMY_DATABASE_URI"] = connection
db = SQLAlchemy(app)

# Create an engine to the database
engine = create_engine(connection, echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
# Base.prepare(db.engine, reflect=True)
Base.prepare(engine, reflect=True)

# Save references to each table
earthquakes = Base.classes.earthquakes
sig_earthquakes = Base.classes.significant_earthquakes
tornadoes = Base.classes.tornadoes
hail = Base.classes.hail
wind = Base.classes.wind
tsunamis = Base.classes.tsunamis
volcanoes = Base.classes.volcanoes

# Create a session
session = Session(bind=engine)

#################################################
# CONVERT SQLALCHEMY TO PYTHON DICTIONARY
#################################################  

def create_earthquake_dict(r):
    return {
    "magnitude" : float(r[0]),
    "place": r[1],
    "time": int(r[2]),
    "timezone": float(r[3]),
    "url": r[4],
    "tsunami" :  int(r[5]),
    "ids" : r[6],
    "specific_type" :  r[7],
    "geometry" :  r[8],
    "lat" : float(r[9]),
    "lng" :  float(r[10]),
    "depth" :  float(r[11])
    }

def create_sig_earthquake_dict(r):
    return {
    "id" : r[0],
    "yr": int(r[1]),
    "month": int(r[2]),
    "day": int(r[3]),
    "hr": int(r[4]),
    "minute" :  int(r[5]),
    "eq_mag_primary" : float(r[6]),
    "intensity" :  r[7],
    "country" :  r[8],
    "location_name" : r[9],
    "lat" :  float(r[10]),
    "lng" :  float(r[11]),
    "deaths" :  int(r[12]),
    "damage_millions" : float(r[13]),
    "total_deaths" :  int(r[14]),
    "total_injuries" :  r[15],
    "total_damage_millions" : r[16]
    }

def create_tornadoes_dict(r):
    return {
    "id": int(r[0]),
    "year" : int(r[1]),
    "month": int(r[2]),
    "day": int(r[3]),
    "date": r[4],
    "time": r[5],
    "timezone" :  int(r[6]),
    "state" : r[7],
    "state_fips" :  int(r[8]),
    "state_nbr" :  int(r[9]),
    "mag" : int(r[10]),
    "injuries" :  int(r[11]),
    "deaths" :  int(r[12]),
    "damage" :  float(r[13]),
    "crop_loss" : float(r[14]),
    "s_lat": float(r[15]),
    "s_lng": float(r[16]),
    "e_lat": float(r[17]),
    "e_lng": float(r[18]),
    "length_traveled": float(r[19]),
    "width": int(r[20]),
    "nbr_states_affected": int(r[21]),
    "sn": int(r[22]),
    "sg": int(r[23]),
    "fa": int(r[24]),
    "fb": int(r[25]),
    "fc": int(r[26]),
    "fd": int(r[27]),
    "fe": int(r[28])
    }

def create_hail_dict(r):
    return {
    "id": int(r[0]),
    "year" : int(r[1]),
    "month": int(r[2]),
    "day": int(r[3]),
    "date": r[4],
    "time": r[5],
    "timezone" :  int(r[6]),
    "state" : r[7],
    "state_fips" :  int(r[8]),
    "state_nbr" :  int(r[9]),
    "mag" : int(r[10]),
    "injuries" :  int(r[11]),
    "deaths" :  int(r[12]),
    "damage" :  float(r[13]),
    "crop_loss" : float(r[14]),
    "s_lat": float(r[15]),
    "s_lng": float(r[16]),
    "e_lat": float(r[17]),
    "e_lng": float(r[18]),
    "fa": float(r[19])
    }

def create_wind_dict(r):
    return {
    "id": int(r[0]),
    "year" : int(r[1]),
    "month": int(r[2]),
    "day": int(r[3]),
    "date": r[4],
    "time": r[5],
    "timezone" :  int(r[6]),
    "state" : r[7],
    "state_fips" :  int(r[8]),
    "state_nbr" :  int(r[9]),
    "mag" : int(r[10]),
    "injuries" :  int(r[11]),
    "deaths" :  int(r[12]),
    "damage" :  float(r[13]),
    "crop_loss" : float(r[14]),
    "s_lat": float(r[15]),
    "s_lng": float(r[16]),
    "e_lat": float(r[17]),
    "e_lng": float(r[18]),
    "fa" : int(r[19]),
    "mag_type": r[20]
    }


def create_tsunami_dict(r):
    return {
    "year" : int(r[0]),
    "month": int(r[1]),
    "day": int(r[2]),
    "hour": int(r[3]),
    "min": r[4],
    "second" :  r[5],
    "validity" : r[6],
    "source" :  r[7],
    "earthquake_mag" :  float(r[8]),
    "country" : r[9],
    "name" :  r[10],
    "lat": float(r[11]),
    "lng": float(r[12]),
    "water_height" :  float(r[13]),
    "tsunami_mag_lida" :  float(r[14]),
    "tsunami_intensity" : float(r[15]),
    "death_nbr": int(r[16]),
    "injuries_nbr": int(r[17]),
    "damage_mill": float(r[18]),
    "damage_code": int(r[19]),
    "house_destroyed": r[20],
    "house_code": int(r[21])
    }


def create_volcanoes_dict(r):
    return {
    "year" : int(r[0]),
    "month": int(r[1]),
    "day": int(r[2]),
    "tsu": int(r[3]),
    "eq": r[4],
    "name" :  r[5],
    "location" : r[6],
    "country" :  r[7],
    "lat": float(r[8]),
    "lng": float(r[9]),    
    "elevation" :  float(r[10]),
    "type" : r[11],
    "volcanic_index" : int(r[12]),
    "fatality_cause": r[13],
    "death": int(r[14]),
    "death_code" : int(r[15]),
    "injuries" : int(r[16]),
    "injuries_code" : int(r[17]),
    "damage": float(r[18]),
    "damage_code": int(r[19]),
    "houses": r[20],
    "houses_code": int(r[21])
    }

#################################################
# Flask Routes
#################################################  
    
# Renders index page
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

# Returns a list of all the cuisine categories
@app.route("/magnitudes")
def magnitudes():
    """Return a list of earthquake magnitudes"""
    magnitudes = db.session.query(earthquakes.magnitude.distinct()).all()
    print(magnitudes)

    # converts a list of list into a single list (flattens list)
    earthquake_list = [item for sublist in list(magnitudes) for item in sublist]

    # return a list of column names (sample names)
    print(earthquake_list)
    float_earthquakes = [float(x) for x in earthquake_list]
    print(float_earthquakes)
    return jsonify(earthquake_list)

# ************************************
# RETURNS ALL EARTHQUAKES FROM EARTHQUAKE TABLE
# ************************************
@app.route("/earthquakes", methods=['GET'])
def return_all_earthquakes():
    # returns a list of restaurants within a given cuisine category

    # Step 1: set up columns needed for this run
    sel = [earthquakes.magnitude, earthquakes.place, earthquakes.time, earthquakes.timezone, earthquakes.url, earthquakes.tsunami, earthquakes.ids, earthquakes.specific_type, earthquakes.geometry, earthquakes.lat, earthquakes.lng, earthquakes.depth]


    # Step 2: Run and store filtered query in results variable 
    all_results = db.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the restaurants in a given cuisine category
    all_earthquakes = []

    for r in all_results:
        transformed_dict = create_earthquake_dict(r)
        all_earthquakes.append(transformed_dict)
    
    print(all_earthquakes)

    return jsonify(all_earthquakes)


# ************************************
# RETURNS ALL EARTHQUAKES FROM EARTHQUAKE TABLE
# ************************************
@app.route("/significant_earthquakes", methods=['GET'])
def return_all_significant_earthquakes():
    # returns a list of restaurants within a given cuisine category

    # Step 1: set up columns needed for this run
    sel = [sig_earthquakes.id, sig_earthquakes.yr, sig_earthquakes.month, sig_earthquakes.day, sig_earthquakes.hr, sig_earthquakes.minute, sig_earthquakes.eq_mag_primary, sig_earthquakes.intensity, sig_earthquakes.country, sig_earthquakes.location_name, sig_earthquakes.lat, sig_earthquakes.lng, sig_earthquakes.deaths, sig_earthquakes.damage_millions, sig_earthquakes.total_deaths, sig_earthquakes.total_injuries, sig_earthquakes.total_damage_millions]


    # Step 2: Run and store filtered query in results variable 
    # all_sig_results = db.session.query(*sel).all()
    all_sig_results = session.query(*sel).all()


    # Step 3: Build a list of dictionary that contains all the restaurants in a given cuisine category
    all_sig_earthquakes = []
    for r in all_sig_results:
        transformed_dict = create_sig_earthquake_dict(r)
        all_sig_earthquakes.append(transformed_dict)
    
    print(all_sig_earthquakes)

    return jsonify(all_sig_earthquakes)


# ************************************
# RETURNS ALL TORNADOES FROM TORNADOES DATA TABLE
# ************************************
@app.route("/tornadoes", methods=['GET'])
def return_all_tornadoes():
    # returns a list of restaurants within a given cuisine category

    # Step 1: set up columns needed for this run
    sel = [tornadoes.id, tornadoes.year, tornadoes.month, tornadoes.day, tornadoes.date, tornadoes.time, tornadoes.timezone, tornadoes.state, tornadoes.state_fips, tornadoes.state_nbr, tornadoes.mag, tornadoes.injuries, tornadoes.deaths, tornadoes.damage, tornadoes.crop_loss, tornadoes.s_lat, tornadoes.s_lng, tornadoes.e_lat, tornadoes.e_lng, tornadoes.length_traveled, tornadoes.width, tornadoes.nbr_states_affected, tornadoes.sn, tornadoes.sg, tornadoes.fa, tornadoes.fb, tornadoes.fc, tornadoes.fd, tornadoes.fe]


    # Step 2: Run and store filtered query in results variable 
    # tornadoes_results = db.session.query(*sel).all()
    tornadoes_results = session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the restaurants in a given cuisine category
    all_tornadoes = []

    for r in tornadoes_results:
        transformed_dict = create_tornadoes_dict(r)
        all_tornadoes.append(transformed_dict)
    
    print(all_tornadoes)

    return jsonify(all_tornadoes)

# ************************************
# RETURNS ALL HAIL FROM HAILS TABLE
# ************************************
@app.route("/hail", methods=['GET'])
def return_all_hail():
    # returns a list of restaurants within a given cuisine category

    # Step 1: set up columns needed for this run
    sel = [hail.id, hail.year, hail.month, hail.day, hail.date, hail.time, hail.timezone, hail.state, hail.state_fips, hail.state_nbr, hail.mag, hail.injuries, hail.deaths, hail.damage, hail.crop_loss, hail.s_lat, hail.s_lng, hail.e_lat, hail.e_lng, hail.fa]


    # Step 2: Run and store filtered query in results variable 
    # hail_results = db.session.query(*sel).all()
    hail_results = session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the restaurants in a given cuisine category
    all_hail = []

    for r in hail_results:
        transformed_dict = create_hail_dict(r)
        all_hail.append(transformed_dict)
    
    print(all_hail)

    return jsonify(all_hail)


# ************************************
# RETURNS ALL WIND FROM WIND TABLE
# ************************************
@app.route("/wind", methods=['GET'])
def return_all_wind():
    # returns a list of restaurants within a given cuisine category

    # Step 1: set up columns needed for this run
    sel = [wind.id, wind.year, wind.month, wind.day, wind.date, wind.time, wind.timezone, wind.state, wind.state_fips, wind.state_nbr, wind.mag, wind.injuries, wind.deaths, wind.damage, wind.crop_loss, wind.s_lat, wind.s_lng, wind.e_lat, wind.e_lng, wind.fa, wind.mag_type]

    # Step 2: Run and store filtered query in results variable 
    # wind_results = db.session.query(*sel).all()
    wind_results = session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the restaurants in a given cuisine category
    all_wind = []

    for r in wind_results:
        transformed_dict = create_wind_dict(r)
        all_wind.append(transformed_dict)
    
    print(all_wind)

    return jsonify(all_wind)

# ************************************
# RETURNS ALL TSUNAMI FROM TSUNAMI TABLE
# ************************************
@app.route("/tsunamis", methods=['GET'])
def return_all_tsunamis():
    # returns a list of restaurants within a given cuisine category

    # Step 1: set up columns needed for this run
    sel = [tsunamis.year, tsunamis.month, tsunamis.day, tsunamis.hour, tsunamis.min, tsunamis.second, tsunamis.validity, tsunamis.source, tsunamis.earthquake_mag, tsunamis.country, tsunamis.name, tsunamis.lat, tsunamis.lng, tsunamis.water_height, tsunamis.tsunami_mag_lida, tsunamis.tsunami_intensity, tsunamis.death_nbr, tsunamis.injuries_nbr, tsunamis.damage_mill, tsunamis.damage_code, tsunamis.house_destroyed, tsunamis.house_code]

    # Step 2: Run and store filtered query in results variable 
    # tsunamis_results = db.session.query(*sel).all()
    tsunamis_results = session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the restaurants in a given cuisine category
    all_tsunamis = []

    for r in tsunamis_results:
        transformed_dict = create_tsunami_dict(r)
        all_tsunamis.append(transformed_dict)
    
    print(all_tsunamis)

    return jsonify(all_tsunamis)

# ************************************
# RETURNS ALL VOLCANOES FROM VOLCANOE TABLE
# ************************************
@app.route("/volcanoes", methods=['GET'])
def return_all_volcanoes():
    # returns a list of restaurants within a given cuisine category

    # Step 1: set up columns needed for this run
    sel = [volcanoes.year, volcanoes.month, volcanoes.day, volcanoes.tsu, volcanoes.eq, volcanoes.name, volcanoes.location, volcanoes.country, volcanoes.lat, volcanoes.lng, volcanoes.elevation,  volcanoes.type, volcanoes.volcanic_index, volcanoes.fatality_cause, volcanoes.death, volcanoes.death_code, volcanoes.injuries, volcanoes.injuries_code, volcanoes.damage, volcanoes.damage_code, volcanoes.houses, volcanoes.houses_code]

    # Step 2: Run and store filtered query in results variable 
    # volcanoes_results = db.session.query(*sel).all()
    volcanoes_results = session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the restaurants in a given cuisine category
    all_vocanoes = []

    for r in volcanoes_results:
        transformed_dict = create_volcanoes_dict(r)
        all_vocanoes.append(transformed_dict)
    
    print(all_vocanoes)

    return jsonify(all_vocanoes)

if __name__ == "__main__":
    app.run()
