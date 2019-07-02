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
    "ids" : r[6],
    "specific_type" :  r[7],
    "geometry" :  r[8],
    "country" : r[9],
    "lat" : float(r[10]),
    "lng" :  float(r[11]),
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
# Functions
#################################################  

def get_all_earthquakes(sql_to_py):

    # Step 1: set up columns needed for this run
    sel = [db_conn.earthquakes.magnitude, db_conn.earthquakes.place, db_conn.earthquakes.time, db_conn.earthquakes.timezone, db_conn.earthquakes.url, db_conn.earthquakes.tsunami, db_conn.earthquakes.ids, db_conn.earthquakes.specific_type, db_conn.earthquakes.geometry, db_conn.earthquakes.country_de, db_conn.earthquakes.lng, db_conn.earthquakes.lat, db_conn.earthquakes.depth]


    # Step 2: Run and store filtered query in results variable 
    all_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the earthquakes
    all_earthquakes = []

    for r in all_results:
        transformed_dict = sql_to_py(r)
        all_earthquakes.append(transformed_dict)
    
    return (all_earthquakes)

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

# Returns a list of all the cuisine categories
@app.route("/magnitudes")
def magnitudes():
    """Return a list of earthquake magnitudes"""
    magnitudes = db_conn.session.query(db_conn.earthquakes.magnitude.distinct()).all()
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

    return jsonify(get_all_earthquakes(create_earthquake_dict))

# ************************************
# RETURNS ALL EARTHQUAKES FROM EARTHQUAKE TABLE
# IN GEOJSON FORMAT
# ************************************
@app.route("/earthquakes-geojson", methods=['GET'])
def return_all_earthquakes_geojson():
    
    geojson_obj = {}

    geojson_obj['type'] = 'FeatureCollection'
    geojson_obj['features'] = get_all_earthquakes(create_eq_geojson_dict)
    geojson_obj['metadata'] = { 'count' : len(geojson_obj['features']) }

    return jsonify(geojson_obj)

# ************************************
# RETURNS ALL EARTHQUAKES FROM EARTHQUAKE TABLE
# ************************************
@app.route("/significant_earthquakes", methods=['GET'])
def return_all_significant_earthquakes():

    # Step 1: set up columns needed for this run
    
    sel = [db_conn.significant_earthquakes.db_id, db_conn.significant_earthquakes.yr,db_conn.significant_earthquakes.month, db_conn.significant_earthquakes.day, db_conn.significant_earthquakes.hr, db_conn.significant_earthquakes.minute, db_conn.significant_earthquakes.eq_mag_primary, db_conn.significant_earthquakes.depth, db_conn.significant_earthquakes.intensity, db_conn.significant_earthquakes.country, db_conn.significant_earthquakes.location_name, db_conn.significant_earthquakes.lat, db_conn.significant_earthquakes.lng, db_conn.significant_earthquakes.deaths, db_conn.significant_earthquakes.damage_millions, db_conn.significant_earthquakes.total_deaths, db_conn.significant_earthquakes.total_injuries, db_conn.significant_earthquakes.total_damage_millions]
    
    print(sel)


    # Step 2: Run and store filtered query in results variable 
    all_sig_results = db_conn.session.query(*sel).all()
    print(all_sig_results)

    # Step 3: Build a list of dictionary that contains all the earthquakes
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

    # Step 1: set up columns needed for this run
    sel = [db_conn.tornadoes.id, db_conn.tornadoes.year, db_conn.tornadoes.month, db_conn.tornadoes.day, db_conn.tornadoes.date, db_conn.tornadoes.time, db_conn.tornadoes.timezone, db_conn.tornadoes.state, db_conn.tornadoes.state_fips, db_conn.tornadoes.state_nbr, db_conn.tornadoes.mag, db_conn.tornadoes.injuries, db_conn.tornadoes.deaths, db_conn.tornadoes.damage, db_conn.tornadoes.crop_loss, db_conn.tornadoes.s_lat, db_conn.tornadoes.s_lng, db_conn.tornadoes.e_lat, db_conn.tornadoes.e_lng, db_conn.tornadoes.length_traveled, db_conn.tornadoes.width, db_conn.tornadoes.nbr_states_affected, db_conn.tornadoes.sn, db_conn.tornadoes.sg, db_conn.tornadoes.fa, db_conn.tornadoes.fb, db_conn.tornadoes.fc, db_conn.tornadoes.fd, db_conn.tornadoes.fe]


    # Step 2: Run and store filtered query in results variable 
    tornadoes_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the tornadoes
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

    # Step 1: set up columns needed for this run
    sel = [db_conn.hail.id, db_conn.hail.year, db_conn.hail.month, db_conn.hail.day, db_conn.hail.date, db_conn.hail.time, db_conn.hail.timezone, db_conn.hail.state, db_conn.hail.state_fips, db_conn.hail.state_nbr, db_conn.hail.mag, db_conn.hail.injuries, db_conn.hail.deaths, db_conn.hail.damage, db_conn.hail.crop_loss, db_conn.hail.s_lat, db_conn.hail.s_lng, db_conn.hail.e_lat, db_conn.hail.e_lng, db_conn.hail.fa]


    # Step 2: Run and store filtered query in results variable 
    hail_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the hail storms
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

    # Step 1: set up columns needed for this run
    sel = [db_conn.wind.id, db_conn.wind.year, db_conn.wind.month, db_conn.wind.day, db_conn.wind.date, db_conn.wind.time, db_conn.wind.timezone, db_conn.wind.state, db_conn.wind.state_fips, db_conn.wind.state_nbr, db_conn.wind.mag, db_conn.wind.injuries, db_conn.wind.deaths, db_conn.wind.damage, db_conn.wind.crop_loss, db_conn.wind.s_lat, db_conn.wind.s_lng, db_conn.wind.e_lat, db_conn.wind.e_lng, db_conn.wind.fa, db_conn.wind.mag_type]

    # Step 2: Run and store filtered query in results variable 
    wind_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the damaging wind events
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

    # Step 1: set up columns needed for this run
    sel = [db_conn.tsunamis.year, db_conn.tsunamis.month, db_conn.tsunamis.day, db_conn.tsunamis.hour, db_conn.tsunamis.min, db_conn.tsunamis.second, db_conn.tsunamis.validity, db_conn.tsunamis.source, db_conn.tsunamis.earthquake_mag, db_conn.tsunamis.country, db_conn.tsunamis.name, db_conn.tsunamis.lat, db_conn.tsunamis.lng, db_conn.tsunamis.water_height, db_conn.tsunamis.tsunami_mag_lida, db_conn.tsunamis.tsunami_intensity, db_conn.tsunamis.death_nbr, db_conn.tsunamis.injuries_nbr, db_conn.tsunamis.damage_mill, db_conn.tsunamis.damage_code, db_conn.tsunamis.house_destroyed, db_conn.tsunamis.house_code]

    # Step 2: Run and store filtered query in results variable 
    tsunamis_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the tsunamis
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

    # Step 1: set up columns needed for this run
    sel = [db_conn.volcanoes.year, db_conn.volcanoes.month, db_conn.volcanoes.day, db_conn.volcanoes.tsu, db_conn.volcanoes.eq, db_conn.volcanoes.name, db_conn.volcanoes.location, db_conn.volcanoes.country, db_conn.volcanoes.lat, db_conn.volcanoes.lng, db_conn.volcanoes.elevation,  db_conn.volcanoes.type, db_conn.volcanoes.volcanic_index, db_conn.volcanoes.fatality_cause, db_conn.volcanoes.death, db_conn.volcanoes.death_code, db_conn.volcanoes.injuries, db_conn.volcanoes.injuries_code, db_conn.volcanoes.damage, db_conn.volcanoes.damage_code, db_conn.volcanoes.houses, db_conn.volcanoes.houses_code]

    # Step 2: Run and store filtered query in results variable 
    volcanoes_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the valcano activity
    all_vocanoes = []

    for r in volcanoes_results:
        transformed_dict = create_volcanoes_dict(r)
        all_vocanoes.append(transformed_dict)
    
    print(all_vocanoes)

    return jsonify(all_vocanoes)

# ************************************
# RETURNS ALL WARNING ALERTS FROM WARNINGS TABLE
# ************************************
@app.route("/warnings", methods=['GET'])
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
    
    print(all_warning_updates)

    return jsonify(all_warning_updates)

# ************************************
# MACHINE LEARNING ROUTE
# ************************************
@app.route("/machine-learning", methods=['GET'])
def machine_learning():
    
    # Step 1: set up columns needed for this run

    sel = [db_conn.earthquakes.magnitude, db_conn.earthquakes.place, db_conn.earthquakes.time, db_conn.earthquakes.timezone, db_conn.earthquakes.url, db_conn.earthquakes.tsunami, db_conn.earthquakes.ids, db_conn.earthquakes.specific_type, db_conn.earthquakes.geometry, db_conn.earthquakes.country_de, db_conn.earthquakes.lng, db_conn.earthquakes.lat, db_conn.earthquakes.depth]


    # Step 2: Run and store filtered query in results variable 
    all_results = db_conn.session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the earthquakes
    all_earthquakes = []

    for r in all_results:
        transformed_dict = create_earthquake_dict(r)
        all_earthquakes.append(transformed_dict)
    
    
    df = pd.DataFrame(all_earthquakes)
    print(df)

    DROP_COLUMNS = ["ids", "geometry", "place", "url", "country", "specific_type", "timezone", "time", "depth"]
    lat_lng_mag_tsu = df.drop(DROP_COLUMNS, axis = 1)

    y = lat_lng_mag_tsu["tsunami"].values
    X = lat_lng_mag_tsu.drop('tsunami', axis=1).values

    X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=42)

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
    
    kneighbor_analysis_dict =  {"Accuracy" : training_accuracy, "test_accuracy": test_accuracy}

    return jsonify(kneighbor_analysis_dict)


if __name__ == "__main__":
    app.run()

