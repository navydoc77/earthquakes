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

url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

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

    cursor.execute("DROP TABLE IF EXISTS earthquakes")
    cursor.execute("DROP TABLE IF EXISTS significant_earthquakes")
    cursor.execute("DROP TABLE IF EXISTS tornadoes")
    cursor.execute("DROP TABLE IF EXISTS hail")
    cursor.execute("DROP TABLE IF EXISTS wind")
    cursor.execute("DROP TABLE IF EXISTS tsunamis")
    cursor.execute("DROP TABLE IF EXISTS volcanoes")

    engine = create_engine('mysql+pymysql://root:root@127.0.0.1/natural_disasterdb', echo=False)

    # Response
    response = requests.get(url).json()

    # Write json file from api call
    with open('all_earthquakes.json', 'w') as json_file:  
        json.dump(response, json_file)

    with open('all_earthquakes.json', 'r') as JSON:
        dict = json.load(JSON)
    
    earthquake_dict = []
    earthquakes = response["features"]
    
    def is_valid(r):
        return (
        r["properties"]['mag'] != None and
        r["properties"]['place'] != None and
        r["properties"]['time'] != None and
        r["properties"]['tz'] != None and
        r["properties"]['url'] != None and
        r["properties"]['tsunami'] != None and
        r["properties"]['ids'] != None and
        r["properties"]['type'] != None and
        r["properties"]['title'] != None and
        r["geometry"]['coordinates'][0] != None and
        r["geometry"]['coordinates'][1] != None and
        r["geometry"]['coordinates'][2] != None)

    def create_dict(r):
        return {
        "magnitude": r["properties"]['mag'],
        "place": r["properties"]['place'],
        "time": r["properties"]['time'],
        "timezone": r["properties"]['tz'],
        "url": r["properties"]['url'],
        "tsunami": r["properties"]['tsunami'],
        "ids": r["properties"]['ids'],
        "specific_type": r["properties"]['type'], 
        "geometry": r["properties"]['title'],
        "lat": r["geometry"]['coordinates'][0],
        "lng": r["geometry"]['coordinates'][1],
        'depth': r["geometry"]['coordinates'][2]
        }

    for r in earthquakes:
        if is_valid(r):
            transformed_dict = create_dict(r)
            earthquake_dict.append(transformed_dict)

            # cleans up the ids column removes commas
    for i in earthquake_dict: 
        value = i["ids"]
        formated_value = value.replace(',', '')
        i["ids"] = formated_value

    ## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'


    #################################################
    # CREATE TABLES
    #################################################
    cursor.execute("CREATE TABLE IF NOT EXISTS earthquakes (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, magnitude VARCHAR(255), place VARCHAR(255), time VARCHAR(255), timezone VARCHAR(255), url VARCHAR(255), tsunami INT(1), ids VARCHAR(255), specific_type VARCHAR(255), geometry VARCHAR(255), lat DECIMAL(10, 6), lng DECIMAL(10,6), depth DECIMAL(6,2)) ENGINE=InnoDB")
    
    # Create table significant earthquake table
    cursor.execute("CREATE TABLE IF NOT EXISTS significant_earthquakes (db_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, id VARCHAR(255), yr INT(5), month INT(3), day INT(3), hr INT(3), minute INT(2), eq_mag_primary DECIMAL(4,2), intensity VARCHAR(255), country VARCHAR(255), location_name VARCHAR(255), lat DECIMAL(10, 6), lng DECIMAL(10,6), deaths INT(10), damage_millions VARCHAR(255), total_deaths INT(10), total_injuries VARCHAR(255), total_damage_millions VARCHAR(255)) ENGINE=InnoDB")
    
    # Create table tornadoes table
    cursor.execute("CREATE TABLE IF NOT EXISTS tornadoes (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, id INT(11), year INT(4), month INT(4), day  INT(4), date VARCHAR(255), time VARCHAR(255), timezone INT(2), state VARCHAR(255), state_fips INT(2), state_nbr INT(4), mag INT(2), injuries INT(4), deaths INT(4), damage DECIMAL(20, 10), crop_loss DECIMAL(20, 10) ,s_lat DECIMAL(10, 6), s_lng DECIMAL(10, 6), e_lat DECIMAL(10, 6), e_lng DECIMAL(10, 6), length_traveled DECIMAL(10, 6), width INT(5), nbr_states_affected INT(2), sn INT(2), sg INT(2), fa INT(4), fb INT(4), fc INT(4), fd INT(4), fe INT(2)) ENGINE=InnoDB")
    
    # Create table hail table
    cursor.execute("CREATE TABLE IF NOT EXISTS hail (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, id INT(11), year INT(4), month INT(4), day  INT(4), date VARCHAR(255), time VARCHAR(255), timezone INT(2), state VARCHAR(255), state_fips INT(2), state_nbr INT(4), mag DECIMAL(5,2), injuries INT(4), deaths INT(4), damage DECIMAL(15, 1), crop_loss DECIMAL(15, 1), s_lat DECIMAL(10, 6), s_lng DECIMAL(10, 6), e_lat DECIMAL(10, 6), e_lng DECIMAL(10, 6), fa INT(4)) ENGINE=InnoDB")
    
    # Create table earthquake wind
    cursor.execute("CREATE TABLE IF NOT EXISTS wind (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, id INT(11), year INT(4), month INT(4), day  INT(4), date VARCHAR(255), time VARCHAR(255), timezone INT(2), state VARCHAR(255), state_fips INT(2), state_nbr INT(4), mag DECIMAL(5,2), injuries INT(4), deaths INT(4), damage DECIMAL(15, 1), crop_loss DECIMAL(15, 1), s_lat DECIMAL(10, 6), s_lng DECIMAL(10, 6), e_lat DECIMAL(10, 6), e_lng DECIMAL(10, 6), fa INT(4), mag_type VARCHAR(255))ENGINE=InnoDB")
    
    # Create table tsunamis table
    cursor.execute("CREATE TABLE IF NOT EXISTS tsunamis (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, year INT(4), month INT(4), day  INT(4), hour INT(4), min INT(4), second INT(4), validity VARCHAR(255), source VARCHAR(255), earthquake_mag DECIMAL(5,2), country VARCHAR(255), name VARCHAR(255), lat DECIMAL(10, 6), lng DECIMAL(10, 6), water_height DECIMAL(10,2), tsunami_mag_lida DECIMAL(4,1), tsunami_intensity DECIMAL(4,1), death_nbr INT(8), injuries_nbr INT(8), damage_mill DECIMAL(10,3), damage_code INT(2), house_destroyed INT(8), house_code INT(2))ENGINE=InnoDB")
    
    # Create table volcanoes table
    cursor.execute("CREATE TABLE IF NOT EXISTS volcanoes (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, year INT(4), month INT(4), day  INT(4), tsu INT(4), eq INT(4), name VARCHAR(255), location VARCHAR(255), country VARCHAR(255), lat DECIMAL(10, 6), lng DECIMAL(10, 6), elevation DECIMAL(8,2), type VARCHAR(255), volcanic_index INT(2), fatality_cause VARCHAR(255), death INT(6), death_code INT(1), injuries INT(6), injuries_code INT(1), damage DECIMAL(8, 4), damage_code INT(1), houses INT(5), houses_code INT(1))ENGINE=InnoDB")

    #################################################
    # LOAD EARTHQUAKE TABLE
    #################################################
    earthquake_values = []
    def r_listify(v):
        return v["magnitude"], v["place"], v["time"], v["timezone"], v["url"], v["tsunami"], v["ids"], v["specific_type"],  v["geometry"], v["lat"], v["lng"], v["depth"]

    for v in earthquake_dict:
        entry_tuple = r_listify(v)
        earthquake_values.append(entry_tuple) 
    
    ## defining the Query
    query = "INSERT INTO earthquakes (magnitude, place, time, timezone, url, tsunami, ids, specific_type, geometry, lat, lng, depth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    ## storing values in a variable
    values = earthquake_values

    ## executing the query with values
    cursor.executemany(query, values)

    ## to make final output we have to run the 'commit()' method of the database object
    db.commit()
    print(cursor.rowcount, "records inserted")

    #################################################
    # LOAD SIGNIFICANT EARTHQUAKE TABLE
    #################################################
    sig_earthquakes_df = pd.read_csv('resources/ngdc_data.tsv', sep='\t', header=0)
    # Cleans up the data and omits columns we don't need
    drop_columns = ["I_D", "FLAG_TSUNAMI", "SECOND", "FOCAL_DEPTH", "EQ_MAG_MS", "EQ_MAG_MW", "EQ_MAG_MB", "EQ_MAG_ML", "EQ_MAG_MFA", "EQ_MAG_UNK", "STATE", "MISSING", "MISSING_DESCRIPTION", "INJURIES", "INJURIES_DESCRIPTION", "HOUSES_DESTROYED", "HOUSES_DESTROYED_DESCRIPTION", "HOUSES_DAMAGED", "HOUSES_DAMAGED_DESCRIPTION", "TOTAL_DEATHS_DESCRIPTION", "TOTAL_MISSING", "TOTAL_MISSING_DESCRIPTION", "TOTAL_HOUSES_DESTROYED", "TOTAL_INJURIES_DESCRIPTION", "TOTAL_HOUSES_DESTROYED_DESCRIPTION", "TOTAL_HOUSES_DAMAGED", "DAMAGE_DESCRIPTION", "REGION_CODE", "TOTAL_DAMAGE_DESCRIPTION", "DEATHS_DESCRIPTION", "TOTAL_HOUSES_DAMAGED_DESCRIPTION"]
    sig_earthquakes_df = sig_earthquakes_df.drop(drop_columns, axis = 1)
    sig_earthquakes_df = sig_earthquakes_df.rename(index=str, columns={"YEAR": "yr", "MONTH" : "month", "DAY" : "day", 'HOUR' : "hr", 'MINUTE' : "minute", 'EQ_PRIMARY' : "eq_mag_primary", 'INTENSITY' : "intensity", 'COUNTRY' : "country", 'LOCATION_NAME' : "location_name", 'LATITUDE': "lat", 'LONGITUDE' : "lng", 'DEATHS' : "deaths", 'DAMAGE_MILLIONS_DOLLARS' : "damage_millions", 'TOTAL_DEATHS' : "total_deaths", 'TOTAL_INJURIES' : "total_injuries", 'TOTAL_DAMAGE_MILLIONS_DOLLARS' : "total_damage_millions" })

    # LOAD SIGNIFICANT EARTHQUAKE DATA INTO TABLE
    sig_earthquakes_df.to_sql('significant_earthquakes', con=engine, if_exists='append', index = False, index_label = "id")

    # LOAD DATA INTO PANDAS FROM CSV FILES
    df_tornadoes = pd.read_csv('resources/1950-2017_torn.csv')
    df_hail = pd.read_csv('resources/1955-2017_hail.csv')
    df_wind = pd.read_csv('resources/wind.csv')
    df_tsunami = pd.read_csv('resources/tsunami.csv')
    df_volcanoes = pd.read_csv('resources/volcano.csv')

    # LOADING TORNADOES DATA INTO TABLE
    df_tornadoes.to_sql('tornadoes', con=engine, if_exists='append', index = False, index_label = "id")
    # LOADING HAIL DATA INTO TABLE
    df_hail.to_sql('hail', con=engine, if_exists='append', index = False, index_label = "id")
    # LOADING WIND DATA INTO TABLE
    df_wind.to_sql('wind', con=engine, if_exists='append', index = False, index_label = "id")
    # LOADING TSUNAMI DATA INTO TABLE
    df_tsunami.to_sql('tsunamis', con=engine, if_exists='append', index = False, index_label = "tb_id")
    # LOADING VOLCANO DATA INTO TABLE
    df_volcanoes.to_sql('volcanoes', con=engine, if_exists='append', index = False, index_label = "tb_id")


extract_transform_load()