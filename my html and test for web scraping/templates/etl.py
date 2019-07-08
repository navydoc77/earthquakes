# Import dependencies
import requests
import json
import pandas as pd

## Connecting to the database
import mysql.connector as mysql
from decimal import Decimal
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from pandas.io import sql

url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson'
warning_url = 'https://api.weather.gov/alerts/active'

def extract_transform_load(): 

    db = mysql.connect(
        host = "127.0.0.1",
        user = "root",
        passwd = "root"
    )
    cursor = db.cursor()
    cursor.execute("DROP DATABASE IF EXISTS natural_disasterdb")
    cursor.execute("CREATE DATABASE IF NOT EXISTS natural_disasterdb")
    cursor.execute("USE natural_disasterdb")

    engine = create_engine('mysql+pymysql://root:root@127.0.0.1/natural_disasterdb', echo=False)

    # Response
    response = requests.get(url).json()


    #################################################
    # CREATES DICTIONARY FOR WARNINGS ALERT DATA AND CLEANS IT UP
    #################################################

    # Response
    warning_response = requests.get(warning_url).json()
    # Write json file from api call
    with open('all_warning.json', 'w') as json_file:  
        json.dump(warning_response, json_file)

    with open('all_warning.json', 'r') as JSON:
        dict = json.load(JSON)
    
    warnings_dict = []
    warnings = warning_response["features"]

    def is_valid_warning(r):
        return (
        r['id'] != None and
        r['geometry'] != None and
        r['properties']['effective'] != None and
        r['properties']['expires'] != None and
        r['properties']['messageType'] != None and
        r['properties']['severity'] != None and    
        r['properties']['certainty'] != None and
        r['properties']['urgency'] != None and
        r['properties']['event'] != None and
        r['properties']['senderName'] != None and
        r['properties']['headline'] != None and
        r['properties']['description'] != None)

    def create_warnings_dict(r):
        return {
        "warning_id": r['id'],
        "lat" : r['geometry']['coordinates'][0][0][1],
        "lng" : r['geometry']['coordinates'][0][0][0],    
        "effective_time" :  r['properties']['effective'],
        "expiration_time" : r['properties']['expires'],
        "message_type" : r['properties']['messageType'],
        "severity" : r['properties']['severity'],
        "certainty" : r['properties']['certainty'],
        "urgency" : r['properties']['urgency'],
        "events" : r['properties']['event'],
        "warning_source" : r['properties']['senderName'],
        "headlines" : r['properties']['headline'],
        "warning_description" : r['properties']['description']
        }

    for r in warnings:
        if is_valid_warning(r):
            transformed_dict = create_warnings_dict(r)
            warnings_dict.append(transformed_dict)

    # cleans up the ids column removes commas
    for i in warnings_dict: 
        value = i['warning_description']
        formated_value = value.replace('\n', ' ')
        i["warning_description"] = formated_value

    #################################################
    # CREATE TABLES
    #################################################


    cursor.execute("CREATE TABLE IF NOT EXISTS warnings (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, warning_id VARCHAR(255), lat DECIMAL(7,3), lng DECIMAL(7,3), effective_time VARCHAR(255), expiration_time VARCHAR(255), message_type VARCHAR(255), severity VARCHAR(255), certainty VARCHAR(255), urgency VARCHAR(255), events VARCHAR(255), warning_source VARCHAR(255), headlines VARCHAR(255), warning_description TEXT NOT NULL ) ENGINE=InnoDB")

    #################################################
    # LOAD WEATHER WARNINGS TABLE
    #################################################
    # Load earthquake data to earthquake table
    warning_values = []
    def w_listify(v):
        return v["warning_id"], v["lat"], v["lng"], v["effective_time"], v["expiration_time"], v["message_type"], v["severity"], v["certainty"], v["urgency"],  v["events"], v["warning_source"], v["headlines"], v["warning_description"]

    for v in warnings_dict:
        entry_tuple = w_listify(v)
        warning_values.append(entry_tuple) 

    ## defining the Query 
    # area_desc, , %s
    query = "INSERT INTO warnings (warning_id, lat, lng, effective_time, expiration_time, message_type, severity, certainty, urgency, events, warning_source, headlines, warning_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    ## storing values in a variable
    values = warning_values

    ## executing the query with values
    cursor.executemany(query, values)

    ## to make final output we have to run the 'commit()' method of the database object
    db.commit()
    print(cursor.rowcount, "records inserted")

    

