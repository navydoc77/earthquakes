from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.metrics import roc_curve
from sklearn.metrics import confusion_matrix
from sklearn import neighbors

# Import the database connection.
import db_conn


app = Flask(__name__)

#################################################
# CONVERT SQLALCHEMY TO PYTHON DICTIONARY
#################################################  
def create_warning_update_dict(r):
    return {
    "warning_id": r[0],
    "lat" :  float(r[1]),
    "lng" : float(r[2]),
    "effective_time" :  r[3],
    "expiration_time" : r[4],
    "message_type" :r[5],
    "severity" :r[6],
    "certainty" :r[7],
    "urgency" :r[8],
    "events" :r[9],
    "warning_source" :r[10],
    "headlines" :r[11],
    "warning_description" :r[12]
    }

def create_earthquake_dict(r):
    return {
    "magnitude" : float(r[0]),
    "place": r[1],
    "time": int(r[2]),
    "timezone": float(r[3]),
    "url": r[4],
    "tsunami" :  int(r[5]),
    "id" : r[6],
    "specific_type" :  r[7],
    "title" :  r[8],
    "country" : r[9],
    "lat" : float(r[11]),
    "lng" :  float(r[10]),
    "depth" :  float(r[12])
    }

def create_eq_geojson_dict(r):
    return {
        'type' : "Feature",
        'properties' :
        {
            'mag'     : float(r[0]),
            'place'   : r[1],
            'time'    : int(r[2]),
            'tz'      : float(r[3]),
            'url'     : r[4],
            'tsunami' :  int(r[5]),
            'type'    :  r[7],
            'title'   :  r[8]
        },
        'geometry' :
        {
            'type' : 'Point',
            'coordinates' : [
               float(r[10]),
               float(r[11]),
               float(r[12])
            ]
        },
        'id' : r[6]
    }

def create_sig_earthquake_dict(r):
    return {
    "id" : r[0],
    "yr": int(r[1]),
    "month": int(r[2]),
    "day": int(r[3]),
    "hr": int(r[4]),
    "minute" :  int(r[5]),
    "magnitude" : float(r[6]),
    "depth" : int(r[7]),
    "intensity": r[8],
    "country" :  r[9],
    "location_name" : r[10],
    "lat" :  float(r[11]),
    "lng" :  float(r[12]),
    "deaths" :  int(r[13]),
    "damage_millions" : float(r[14]),
    "total_deaths" :  int(r[15]),
    "total_injuries" :  r[16],
    "total_damage_millions" : r[17]
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
    "fe": int(r[28]),
    "dtg": r[29]
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
    "houses_code": int(r[21]),
    "dtg": r[22]
    }

def create_eq_filter_viz(r):
    return {
    "dtg" : r[0],
    "lat": float(r[1]),
    "lng": float(r[2]),
    "mag": float(r[3]),
    "depth": int(r[4])
    }
    
def create_volcano_filter_viz(r):
    return {
    "dtg" : r[0],
    "lat": float(r[1]),
    "lng": float(r[2]),
    "volcanic_index": float(r[3]),
    "death": int(r[4])
    }    

def create_tsunami_filter_viz(r):
    return {
    "dtg" : r[0],
    "lat": float(r[1]),
    "lng": float(r[2]),
    "mag": float(r[3]),
    "water_height": float(r[4])
    }   



#################################################
# Functions
#################################################  

def get_all_earthquakes(sql_to_py):

    # Step 1: set up columns needed for this run
    sel = [db_conn.earthquakes.magnitude, db_conn.earthquakes.place, db_conn.earthquakes.time, db_conn.earthquakes.timezone, db_conn.earthquakes.url, db_conn.earthquakes.tsunami, db_conn.earthquakes.id, db_conn.earthquakes.specific_type, db_conn.earthquakes.title, db_conn.earthquakes.country_de, db_conn.earthquakes.lng, db_conn.earthquakes.lat, db_conn.earthquakes.depth]


    # Step 2: Run and store filtered query in results variable 
    all_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the earthquakes
    all_earthquakes = []

    for r in all_results:
        transformed_dict = sql_to_py(r)
        all_earthquakes.append(transformed_dict)
    
    return (all_earthquakes)


# ############ Machine Learning Function ############### #
# This will produce the data for plotting KNN analysis   #

def kNeighborAnalysis(X, y):

    ################ TRAIN TEST SPLIT ####################
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=42)

    ################ K-NEAREST NEIGHBOR ####################
    training_accuracy = []
    test_accuracy = []
    # try n_neighbors from 1 to 10
    neighbors_settings = range(1, 11)

    for n_neighbors in neighbors_settings:
        # build the model
        clf = KNeighborsClassifier(n_neighbors=n_neighbors)
        clf.fit(X_train, y_train)
        # record training set accuracy
        training_accuracy.append(clf.score(X_train, y_train))
        # record generalization accuracy
        test_accuracy.append(clf.score(X_test, y_test))

    knn_annalysis_dict = {
        "x" : [1,2,3,4,5,6,7,8,9,10],
        "training_scores": training_accuracy,
        "test_scores": test_accuracy}

    return (knn_annalysis_dict)

#################################################
# Flask Routes
#################################################  
    


#*************** WEBPAGES***********************#
# Renders index page
@app.route("/")
def index():
    return render_template('index.html')

# Renders earthquake index page
@app.route("/earthquake-index")
def earthquake_index():
    return render_template('earthquake_index.html')

# Renders ml page
@app.route("/ml-landing")
def ml_machine():
    return render_template('ml_landing.html', data_source_url=url_for('machine_learning'))

# Renders sentiment analysis page
@app.route("/sentiment-landing")
def sentiment_analysis():
    return render_template('sentiment_landing.html')

# Renders sig_earthquakes page
@app.route("/sig_earthquake-landing")
def sig_earthquake():
    return render_template('sig_earthquakes.html')    

# Renders tornadoes page
@app.route("/tornadoes-landing")
def tornadoes_landing():
    return render_template('tornadoes_landing.html') 

# Renders volcanoes page
@app.route("/volcanoes-landing")
def volcanoes_landing():
    return render_template('volcanoes_landing.html') 

# Renders tsunamis page
@app.route("/tsunamis-landing")
def tsunamis_landing():
    return render_template('tsunamis_landing.html')

# Renders wind page
@app.route("/wind-landing")
def wind_landing():
    return render_template('wind_landing.html')

# Renders wind page
@app.route("/hail-landing")
def hail_landing():
    return render_template('hail_landing.html')

# Renders weather warnings page
@app.route("/warnings-landing")
def warnings_landing():
    return render_template('warnings_landing.html')

#*************** WEBPAGES***********************#

# Renders earthquake filter dashboard
@app.route("/earthquake-filter-dashb")
def earthquake_filter_dashb():
    """Return the homepage."""
    return render_template("eq_filter_viz.html")

# Renders tornado filter dashboard    
@app.route("/tornado-filter-dashb")
def tornado_filter_dashb():
    """Return the homepage."""
    return render_template("tornado_filter_dashb.html")    

# Renders volcano filter dashboard
@app.route("/volcano-filter-dashb")
def volcano_filter_dashb():
    """Return the homepage."""
    return render_template("volcano_filter_dashb.html")

# Renders tsunami filter dashboard
@app.route("/tsunami-filter-dashb")
def tsunami_filter_dashb():
    """Return the homepage."""
    return render_template("tsunami_filter_dashb.html")

# EQ Magnitudes
@app.route("/api/magnitudes")
def magnitudes():
    """Return a list of earthquake magnitudes"""
    magnitudes = db_conn.session.query(db_conn.earthquakes.magnitude.distinct()).all()

    # converts a list of list into a single list (flattens list)
    earthquake_list = [item for sublist in list(magnitudes) for item in sublist]

    # return a list of column names (sample names)
    float_earthquakes = [float(x) for x in earthquake_list]
    return jsonify(earthquake_list)

# ************************************
# RETURNS ALL EARTHQUAKES FROM EARTHQUAKE TABLE
# ************************************
@app.route("/api/earthquakes", methods=['GET'])
def return_all_earthquakes():

    return jsonify(get_all_earthquakes(create_earthquake_dict))

# ************************************
# RETURNS ALL EARTHQUAKES FROM EARTHQUAKE TABLE
# IN GEOJSON FORMAT
# ************************************
@app.route("/api/earthquakes-geojson", methods=['GET'])
def return_all_earthquakes_geojson():
    
    geojson_obj = {}

    geojson_obj['type'] = 'FeatureCollection'
    geojson_obj['features'] = get_all_earthquakes(create_eq_geojson_dict)
    geojson_obj['metadata'] = { 'count' : len(geojson_obj['features']) }

    return jsonify(geojson_obj)

# ************************************
# RETURNS ALL EARTHQUAKES FROM EARTHQUAKE TABLE
# ************************************
@app.route("/api/significant_earthquakes", methods=['GET'])
def return_all_significant_earthquakes():

    # Step 1: set up columns needed for this run
    
    sel = [db_conn.significant_earthquakes.tb_id, db_conn.significant_earthquakes.yr,db_conn.significant_earthquakes.month, db_conn.significant_earthquakes.day, db_conn.significant_earthquakes.hr, db_conn.significant_earthquakes.minute, db_conn.significant_earthquakes.eq_mag_primary, db_conn.significant_earthquakes.depth, db_conn.significant_earthquakes.intensity, db_conn.significant_earthquakes.country, db_conn.significant_earthquakes.location_name, db_conn.significant_earthquakes.lat, db_conn.significant_earthquakes.lng, db_conn.significant_earthquakes.deaths, db_conn.significant_earthquakes.damage_millions, db_conn.significant_earthquakes.total_deaths, db_conn.significant_earthquakes.total_injuries, db_conn.significant_earthquakes.total_damage_millions]


    # Step 2: Run and store filtered query in results variable 
    all_sig_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the earthquakes
    all_sig_earthquakes = []
    for r in all_sig_results:
        transformed_dict = create_sig_earthquake_dict(r)
        all_sig_earthquakes.append(transformed_dict)

    return jsonify(all_sig_earthquakes)


# ************************************
# RETURNS ALL EARTHQUAKES FROM EQ_FILTER_VIZ TABLE
# ************************************
@app.route("/api/eq_filter_viz", methods=['GET'])
def return_eq_filter_viz():

    # Step 1: set up columns needed for this run
    
    sel = [db_conn.eq_filter_viz.dtg, db_conn.eq_filter_viz.lat, db_conn.eq_filter_viz.lng, db_conn.eq_filter_viz.mag, db_conn.eq_filter_viz.depth]



    # Step 2: Run and store filtered query in results variable 
    all_eq_filter_viz_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the earthquakes
    all_eq_filter_viz = []
    for r in all_eq_filter_viz_results:
        transformed_dict = create_eq_filter_viz(r)
        all_eq_filter_viz.append(transformed_dict)

    return jsonify(all_eq_filter_viz)

# ************************************
# RETURNS VOLCANO ACTIVITY FROM VOLCANO_FILTER_VIZ TABLE
# ************************************
@app.route("/api/volcano_filter_viz", methods=['GET'])
def return_volcano_filter_viz():

    # Step 1: set up columns needed for this run
    
    sel = [db_conn.volcano_filter_viz.dtg, db_conn.volcano_filter_viz.lat, db_conn.volcano_filter_viz.lng, db_conn.volcano_filter_viz.volcanic_index, db_conn.volcano_filter_viz.death]
    
    # print(sel)


    # Step 2: Run and store filtered query in results variable 
    all_volcano_filter_viz_results = db_conn.session.query(*sel).all()
    # print(all_volcano_filter_viz_results)

    # Step 3: Build a list of dictionary that contains all the earthquakes
    all_volcano_filter_viz = []
    for r in all_volcano_filter_viz_results:
        transformed_dict = create_volcano_filter_viz(r)
        all_volcano_filter_viz.append(transformed_dict)
    
    # print(all_volcano_filter_viz)

    return jsonify(all_volcano_filter_viz)

# ************************************
# RETURNS ALL TSUNAMI FROM TSUNAMI_FILTER_VIZ TABLE
# ************************************
@app.route("/api/tsunami_filter_viz", methods=['GET'])
def return_tsunami_filter_viz():

    # Step 1: set up columns needed for this run
    
    sel = [db_conn.tsunami_filter_viz.dtg, db_conn.tsunami_filter_viz.lat, db_conn.tsunami_filter_viz.lng, db_conn.tsunami_filter_viz.mag, db_conn.tsunami_filter_viz.water_height]
    
    # print(sel)


    # Step 2: Run and store filtered query in results variable 
    all_tsunami_filter_viz_results = db_conn.session.query(*sel).all()
    # print(all_tsunami_filter_viz_results)

    # Step 3: Build a list of dictionary that contains all the earthquakes
    all_tsunami_filter_viz = []
    for r in all_tsunami_filter_viz_results:
        transformed_dict = create_tsunami_filter_viz(r)
        all_tsunami_filter_viz.append(transformed_dict)
    
    # print(all_tsunami_filter_viz)

    return jsonify(all_tsunami_filter_viz)

# ************************************
# RETURNS ALL TORNADOES FROM TORNADOES DATA TABLE
# ************************************
@app.route("/api/tornadoes", methods=['GET'])
def return_all_tornadoes():

    # Step 1: set up columns needed for this run
    sel = [db_conn.tornadoes.id, db_conn.tornadoes.year, db_conn.tornadoes.month, db_conn.tornadoes.day, db_conn.tornadoes.date, db_conn.tornadoes.time, db_conn.tornadoes.timezone, db_conn.tornadoes.state, db_conn.tornadoes.state_fips, db_conn.tornadoes.state_nbr, db_conn.tornadoes.mag, db_conn.tornadoes.injuries, db_conn.tornadoes.deaths, db_conn.tornadoes.damage, db_conn.tornadoes.crop_loss, db_conn.tornadoes.s_lat, db_conn.tornadoes.s_lng, db_conn.tornadoes.e_lat, db_conn.tornadoes.e_lng, db_conn.tornadoes.length_traveled, db_conn.tornadoes.width, db_conn.tornadoes.nbr_states_affected, db_conn.tornadoes.sn, db_conn.tornadoes.sg, db_conn.tornadoes.fa, db_conn.tornadoes.fb, db_conn.tornadoes.fc, db_conn.tornadoes.fd, db_conn.tornadoes.fe, db_conn.tornadoes.dtg]


    # Step 2: Run and store filtered query in results variable 
    tornadoes_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the tornadoes
    all_tornadoes = []

    for r in tornadoes_results:
        transformed_dict = create_tornadoes_dict(r)
        all_tornadoes.append(transformed_dict)
    
    # print(all_tornadoes)

    return jsonify(all_tornadoes)

# ************************************
# RETURNS ALL HAIL FROM HAILS TABLE
# ************************************
@app.route("/api/hail", methods=['GET'])
def return_all_hail():

    # Step 1: set up columns needed for this run
    sel = [db_conn.hail.id, db_conn.hail.year, db_conn.hail.month, db_conn.hail.day, db_conn.hail.date, db_conn.hail.time, db_conn.hail.timezone, db_conn.hail.state, db_conn.hail.state_fips, db_conn.hail.state_nbr, db_conn.hail.mag, db_conn.hail.injuries, db_conn.hail.deaths, db_conn.hail.damage, db_conn.hail.crop_loss, db_conn.hail.s_lat, db_conn.hail.s_lng, db_conn.hail.e_lat, db_conn.hail.e_lng, db_conn.hail.fa]


    # Step 2: Run and store filtered query in results variable 
    hail_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the hail storms
    all_hail = []

    for r in hail_results:
        transformed_dict = create_hail_dict(r)
        all_hail.append(transformed_dict)
    
    # print(all_hail)

    return jsonify(all_hail)


# ************************************
# RETURNS ALL WIND FROM WIND TABLE
# ************************************
@app.route("/api/wind", methods=['GET'])
def return_all_wind():

    # Step 1: set up columns needed for this run
    sel = [db_conn.wind.id, db_conn.wind.year, db_conn.wind.month, db_conn.wind.day, db_conn.wind.date, db_conn.wind.time, db_conn.wind.timezone, db_conn.wind.state, db_conn.wind.state_fips, db_conn.wind.state_nbr, db_conn.wind.mag, db_conn.wind.injuries, db_conn.wind.deaths, db_conn.wind.damage, db_conn.wind.crop_loss, db_conn.wind.s_lat, db_conn.wind.s_lng, db_conn.wind.e_lat, db_conn.wind.e_lng, db_conn.wind.fa, db_conn.wind.mag_type]

    # Step 2: Run and store filtered query in results variable 
    wind_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the damaging wind events
    all_wind = []

    for r in wind_results:
        transformed_dict = create_wind_dict(r)
        all_wind.append(transformed_dict)
    
    # print(all_wind)

    return jsonify(all_wind)

# ************************************
# RETURNS ALL TSUNAMI FROM TSUNAMI TABLE
# ************************************
@app.route("/api/tsunamis", methods=['GET'])
def return_all_tsunamis():

    # Step 1: set up columns needed for this run
    sel = [db_conn.tsunamis.year, db_conn.tsunamis.month, db_conn.tsunamis.day, db_conn.tsunamis.hour, db_conn.tsunamis.min, db_conn.tsunamis.second, db_conn.tsunamis.validity, db_conn.tsunamis.source, db_conn.tsunamis.earthquake_mag, db_conn.tsunamis.country, db_conn.tsunamis.name, db_conn.tsunamis.lat, db_conn.tsunamis.lng, db_conn.tsunamis.water_height, db_conn.tsunamis.tsunami_mag_lida, db_conn.tsunamis.tsunami_intensity, db_conn.tsunamis.death_nbr, db_conn.tsunamis.injuries_nbr, db_conn.tsunamis.damage_mill, db_conn.tsunamis.damage_code, db_conn.tsunamis.house_destroyed, db_conn.tsunamis.house_code]

    # Step 2: Run and store filtered query in results variable 
    tsunamis_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the tsunamis
    all_tsunamis = []

    for r in tsunamis_results:
        transformed_dict = create_tsunami_dict(r)
        all_tsunamis.append(transformed_dict)
    
    # print(all_tsunamis)

    return jsonify(all_tsunamis)

# ************************************
# RETURNS ALL VOLCANOES FROM VOLCANOE TABLE
# ************************************
@app.route("/api/volcanoes", methods=['GET'])
def return_all_volcanoes():

    # Step 1: set up columns needed for this run
    sel = [db_conn.volcanoes.year, db_conn.volcanoes.month, db_conn.volcanoes.day, db_conn.volcanoes.tsu, db_conn.volcanoes.eq, db_conn.volcanoes.name, db_conn.volcanoes.location, db_conn.volcanoes.country, db_conn.volcanoes.lat, db_conn.volcanoes.lng, db_conn.volcanoes.elevation,  db_conn.volcanoes.type, db_conn.volcanoes.volcanic_index, db_conn.volcanoes.fatality_cause, db_conn.volcanoes.death, db_conn.volcanoes.death_code, db_conn.volcanoes.injuries, db_conn.volcanoes.injuries_code, db_conn.volcanoes.damage, db_conn.volcanoes.damage_code, db_conn.volcanoes.houses, db_conn.volcanoes.houses_code]

    # Step 2: Run and store filtered query in results variable 
    volcanoes_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the valcano activity
    all_vocanoes = []

    for r in volcanoes_results:
        transformed_dict = create_volcanoes_dict(r)
        all_vocanoes.append(transformed_dict)
    
    # print(all_vocanoes)

    return jsonify(all_vocanoes)

# ************************************
# RETURNS ALL WARNING ALERTS FROM WARNINGS TABLE
# ************************************
@app.route("/api/warnings", methods=['GET'])
def return_all_warning():

    # Step 1: set up columns needed for this run
    sel = [db_conn.warnings.warning_id,
        db_conn.warnings.lat,
        db_conn.warnings.lng,
        db_conn.warnings.effective_time,
        db_conn.warnings.expiration_time,
        db_conn.warnings.message_type,
        db_conn.warnings.severity,
        db_conn.warnings.certainty,
        db_conn.warnings.urgency,
        db_conn.warnings.events,
        db_conn.warnings.warning_source,
        db_conn.warnings.headlines,
        db_conn.warnings.warning_description,
        ]
    
    # Step 2: Run and store filtered query in results variable
    warning_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the warning updates
    all_warning_updates = []

    for r in warning_results:
        transformed_dict = create_warning_update_dict(r)
        all_warning_updates.append(transformed_dict)
    
    return jsonify(all_warning_updates)


# ************************************
# MACHINE LEARNING ROUTE
# ************************************
@app.route("/api/machine-learning", methods=['GET'])
def machine_learning():

    # Step 1: set up columns needed for this run

    sel = [db_conn.earthquakes.magnitude, db_conn.earthquakes.place, db_conn.earthquakes.time, db_conn.earthquakes.timezone, db_conn.earthquakes.url, db_conn.earthquakes.tsunami, db_conn.earthquakes.id, db_conn.earthquakes.specific_type, db_conn.earthquakes.title, db_conn.earthquakes.country_de, db_conn.earthquakes.lng, db_conn.earthquakes.lat, db_conn.earthquakes.depth]


    # Step 2: Run and store filtered query in results variable 
    all_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the earthquakes
    all_earthquakes = []

    for r in all_results:
        transformed_dict = create_earthquake_dict(r)
        all_earthquakes.append(transformed_dict)
    
    
    df = pd.DataFrame(all_earthquakes)
    
    ################ FEATURES PREPROCESSING FOR KNN MODEL ###################
    DROP_COLUMNS = ["place", "time", "timezone", "url",  "id", "specific_type", "title", "country"]
    knn_df = df.drop(DROP_COLUMNS, axis = 1)

    # **************************************************** #
    # ############### FEATURE SELECTION ################## #
    # **************************************************** #

    # Case 1: LNG, DEPTH, MAG
    # CASE 2: LNG, DEPTH
    # CASE 3: LNG, MAG
    # CASE 4: DEPTH, MAG
    # CASE 5: LNG,
    # CASE 6: DEPTH
    # CASE 7: MAG
    # CASE 8: 
    
    ################# Lat "Lng Depth Magnitude "###############
    # CASE 1: ALL Subfeatures included: Lng Depth Magnitude
    # CASE 1: ALL CHECKED OFF
    # CASE 1: PREFIX DESIGNATION: All

    # Step 1: Drop columns
    # NONE

    # Step 2: Assign X and y values
    y = knn_df["tsunami"].values
    X = knn_df.drop('tsunami', axis=1).values

    # Step 3: Conducted Analysis and store reust in variable
    all_data = kNeighborAnalysis(X,y)

    ################# Lat "Lng Depth" ###############
    # CASE 2: LNG, DEPTH CHECKED OFF
    # CASE 2: MAGNITUDE NOT CHECKED OFF
    # CASE 2: PREFIX DESIGNATION: lng_depth_df

    # Step 1: Drop columns
    CASE2_DROP_COLUMNS = ["magnitude"]
    lng_depth_df = knn_df.drop(CASE2_DROP_COLUMNS, axis = 1)

    # Step 2: Assign X and y values
    y = lng_depth_df["tsunami"].values
    X = lng_depth_df.drop('tsunami', axis=1).values

    # Step 3: Conducted Analysis and store reust in variable
    lng_depth_data = kNeighborAnalysis(X,y)

    ################# Lat "Lng Magnitude" ###############
    # CASE 3: LNG AND MAGNITUDE CHECKED OFF
    # CASE 3: DEPTH NOT CHECKED OFF
    # CASE 3: PREFIX DESIGNATION: lng_magnitude

    # Step 1: Drop columns
    CASE3_DROP_COLUMNS = ["depth"]
    lng_magnitude_df = knn_df.drop(CASE3_DROP_COLUMNS, axis = 1)

    # Step 2: Assign X and y values
    y = lng_magnitude_df["tsunami"].values
    X = lng_magnitude_df.drop('tsunami', axis=1).values

    # Step 3: Conducted Analysis and store reust in variable
    lng_magnitude_data = kNeighborAnalysis(X,y)

    ################# Lat "Depth Magnitude" ###############
    # CASE 4: DEPTH AND MAGNITUDE CHECKED OFF
    # CASE 4: LNG NOT CHECKED OFF
    # CASE 4: PREFIX DESIGNATION: depth_magnitude

    # Step 1: Drop columns
    CASE4_DROP_COLUMNS = ["lng"]
    depth_magnitude_df = knn_df.drop(CASE4_DROP_COLUMNS, axis = 1)

    # Step 2: Assign X and y values
    y = depth_magnitude_df["tsunami"].values
    X = depth_magnitude_df.drop('tsunami', axis=1).values

    # Step 3: Conducted Analysis and store reust in variable
    depth_magnitude_data = kNeighborAnalysis(X,y)

    ################# Lat "Lng" ###############
    # CASE 5: LNG CHECKED OFF
    # CASE 5: MAGNITUDE AND DEPTH NOT CHECKED OFF
    # CASE 5: PREFIX DESIGNATION: lng_df

    # Step 1: Drop columns
    CASE5_DROP_COLUMNS = ["magnitude", "depth"]
    lng_df = knn_df.drop(CASE5_DROP_COLUMNS, axis = 1)

    # Step 2: Assign X and y values
    y = lng_df["tsunami"].values
    X = lng_df.drop('tsunami', axis=1).values

    # Step 3: Conducted Analysis and store reust in variable
    lng_data = kNeighborAnalysis(X,y)

    ################# Lat "Depth" ###############
    # CASE 6: DEPTH CHECKED OFF
    # CASE 6: LNG AND MAG NOT CHECKED OFF
    # CASE 6: PREFIX DESIGNATION: depth

    # Step 1: Drop columns
    CASE6_DROP_COLUMNS = ["magnitude", "lng"]
    depth_df = knn_df.drop(CASE6_DROP_COLUMNS, axis = 1)

    # Step 2: Assign X and y values
    y = depth_df["tsunami"].values
    X = depth_df.drop('tsunami', axis=1).values

    # Step 3: Conducted Analysis and store reust in variable
    depth_data = kNeighborAnalysis(X,y)

    ################# Lat "Magnitude" ###############
    # CASE 7: MAGNITUDE CHECKED OFF
    # CASE 7: LNG DEPTH NOT CHECKED OFF
    # CASE 7: PREFIX DESIGNATION: magnitude

    # Step 1: Drop columns
    CASE5_DROP_COLUMNS = ["depth", "lng"]
    magnitude_df = knn_df.drop(CASE5_DROP_COLUMNS, axis = 1)

    # Step 2: Assign X and y values
    y = magnitude_df["tsunami"].values
    X = magnitude_df.drop('tsunami', axis=1).values

    # Step 3: Conducted Analysis and store reust in variable
    magnitude_data = kNeighborAnalysis(X,y)

    ################# Lat ###############
    # CASE 8: NO FEATURES SELECTED 
    # CASE 8: ALL BOXED UNCHECKED
    # CASE 8: PREFIX DESIGNATION: lat_df

    # Step 1: Drop columns
    DROP_NEW_COLUMNS = ["magnitude", "depth", "lng"]
    lat_df = knn_df.drop(DROP_NEW_COLUMNS, axis = 1)

    # Step 2: Assign X and y values
    y = lat_df["tsunami"].values
    X = lat_df.drop('tsunami', axis=1).values

    # Step 3: Conducted Analysis and store reust in variable
    lat_data = kNeighborAnalysis(X,y)


    ################# RETURNING ALL CASE RESULTS #########################
    all_knn_analysis_data = {
        "case1" : all_data,
        "case2" : lng_depth_data,
        "case3" : lng_magnitude_data,
        "case4" : depth_magnitude_data,
        "case5" : lng_data,
        "case6" : depth_data, 
        "case7" : magnitude_data,
        "case8" : lat_data
    }

    return jsonify(all_knn_analysis_data)


    ################ KNN CONFUSION MATRIX ####################
    # knn = neighbors.KNeighborsClassifier(n_neighbors=5)
    # knn.fit(X_train, y_train)
    # y_pred = knn.predict_proba(X_test)
    # confusion_matrix(y_test, y_pred)

    ################ LOGISTIC REGRESSION ####################
    # logreg = LogisticRegression()
    # logreg.fit(X_train, y_train)
    # y_pred = logreg.predict(X_test)
    # y_pred_prob = logreg.predict_proba(X_test)[:,1]
    # fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
    # log_reg_train_score = logreg.score(X_train, y_train)
    # log_reg_test_score = logreg.score(X_test, y_test)


    ################ RETURNING MACHINE LEARNING DATA ####################
    # ml_data = {
    #     "x" : [1,2,3,4,5,6,7,8,9,10],
    #     "y1": test_accuracy,
    #     "y2": training_accuracy}
        # "fpr": fpr,
        # "tpr": tpr,
        # "thresholds": thresholds,
        # "log_reg_train_score": log_reg_train_score,
        # "log_reg_test_score" : log_reg_test_score

if __name__ == "__main__":
    app.run()



    # ################ TRAIN TEST SPLIT ####################
    # X_train, X_test, y_train, y_test = train_test_split(
    # X, y, random_state=42)

    # ################ K-NEAREST NEIGHBOR ####################
    # all_test_accuracy = []
    # all_training_accuracy = []

    # # try n_neighbors from 1 to 10
    # neighbors_settings = range(1, 11)

    # for n_neighbors in neighbors_settings:
    #     # build the model
    #     clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    #     clf.fit(X_train, y_train)
    #     # record training set accuracy
    #     all_training_accuracy.append(clf.score(X_train, y_train))
    #     # record generalization accuracy
    #     all_test_accuracy.append(clf.score(X_test, y_test))

    # all_data =  {
    #     "x" : [1,2,3,4,5,6,7,8,9,10],
    #     "y1": all_test_accuracy,
    #     "y2": all_training_accuracy}