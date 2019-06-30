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

    # cursor.execute("DROP TABLE IF EXISTS earthquakes")
    # cursor.execute("DROP TABLE IF EXISTS tornadoes")
    # cursor.execute("DROP TABLE IF EXISTS hail")
    # cursor.execute("DROP TABLE IF EXISTS wind")
    # cursor.execute("DROP TABLE IF EXISTS tsunamis")
    # cursor.execute("DROP TABLE IF EXISTS volcanoes")

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
        r['id'] != None and
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
        "id": r['id'],
        "specific_type": r["properties"]['type'], 
        "title": r["properties"]['title'],
        "lat": r["geometry"]['coordinates'][1],
        "lng": r["geometry"]['coordinates'][0],
        'depth': r["geometry"]['coordinates'][2]
        }

    for r in earthquakes:
        if is_valid(r):
            transformed_dict = create_dict(r)
            earthquake_dict.append(transformed_dict)


    #################################################
    # CREATE TABLES
    #################################################

    # Create earthquakes table
    cursor.execute("CREATE TABLE IF NOT EXISTS earthquakes (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, magnitude VARCHAR(255), place VARCHAR(255), time VARCHAR(255), timezone VARCHAR(255), url VARCHAR(255), tsunami INT(1), id VARCHAR(255), specific_type VARCHAR(255), title VARCHAR(255), country_de varchar(80), lng DECIMAL(10, 6), lat DECIMAL(10,6), depth DECIMAL(6,2)) ENGINE=InnoDB")

    # Create significant_earthquakes table
    cursor.execute("CREATE TABLE IF NOT EXISTS significant_earthquakes (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, yr INT(5), month INT(3), day INT(3), hr INT(3), minute INT(2), eq_mag_primary DECIMAL(4,2), depth VARCHAR(255), intensity VARCHAR(255), country VARCHAR(255), location_name VARCHAR(255), lat DECIMAL(10, 6), lng DECIMAL(10,6), deaths INT(10), damage_millions VARCHAR(255), total_deaths INT(10), total_injuries VARCHAR(255), total_damage_millions VARCHAR(255), dtg varchar(25)) ENGINE=InnoDB")
    
    # Create tornadoes table
    cursor.execute("CREATE TABLE IF NOT EXISTS tornadoes (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, id INT(11), year INT(4), month INT(4), day  INT(4), date VARCHAR(255), time VARCHAR(255), timezone INT(2), state VARCHAR(255), state_fips INT(2), state_nbr INT(4), mag INT(2), injuries INT(4), deaths INT(4), damage DECIMAL(20, 10), crop_loss DECIMAL(20, 10) ,s_lat DECIMAL(10, 6), s_lng DECIMAL(10, 6), e_lat DECIMAL(10, 6), e_lng DECIMAL(10, 6), length_traveled DECIMAL(10, 6), width INT(5), nbr_states_affected INT(2), sn INT(2), sg INT(2), fa INT(4), fb INT(4), fc INT(4), fd INT(4), fe INT(2), dtg varchar(25)) ENGINE=InnoDB")
    
    # Create hail table
    cursor.execute("CREATE TABLE IF NOT EXISTS hail (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, id INT(11), year INT(4), month INT(4), day  INT(4), date VARCHAR(255), time VARCHAR(255), timezone INT(2), state VARCHAR(255), state_fips INT(2), state_nbr INT(4), mag DECIMAL(5,2), injuries INT(4), deaths INT(4), damage DECIMAL(15, 1), crop_loss DECIMAL(15, 1), s_lat DECIMAL(10, 6), s_lng DECIMAL(10, 6), e_lat DECIMAL(10, 6), e_lng DECIMAL(10, 6), fa INT(4)) ENGINE=InnoDB")
    
    # Create wind table
    cursor.execute("CREATE TABLE IF NOT EXISTS wind (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, id INT(11), year INT(4), month INT(4), day  INT(4), date VARCHAR(255), time VARCHAR(255), timezone INT(2), state VARCHAR(255), state_fips INT(2), state_nbr INT(4), mag DECIMAL(5,2), injuries INT(4), deaths INT(4), damage DECIMAL(15, 1), crop_loss DECIMAL(15, 1), s_lat DECIMAL(10, 6), s_lng DECIMAL(10, 6), e_lat DECIMAL(10, 6), e_lng DECIMAL(10, 6), fa INT(4), mag_type VARCHAR(255))ENGINE=InnoDB")
    
    # Create tsunamis table
    cursor.execute("CREATE TABLE IF NOT EXISTS tsunamis (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, year INT(4), month INT(4), day  INT(4), hour INT(4), min INT(4), second INT(4), validity VARCHAR(255), source VARCHAR(255), earthquake_mag DECIMAL(5,2), country VARCHAR(255), name VARCHAR(255), lat DECIMAL(10, 6), lng DECIMAL(10, 6), water_height DECIMAL(10,2), tsunami_mag_lida DECIMAL(4,1), tsunami_intensity DECIMAL(4,1), death_nbr INT(8), injuries_nbr INT(8), damage_mill DECIMAL(10,3), damage_code INT(2), house_destroyed INT(8), house_code INT(2))ENGINE=InnoDB")
    
    # Create volcanoes table
    cursor.execute("CREATE TABLE IF NOT EXISTS volcanoes (tb_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, year INT(4), month INT(4), day  INT(4), tsu INT(4), eq INT(4), name VARCHAR(255), location VARCHAR(255), country VARCHAR(255), lat DECIMAL(10, 6), lng DECIMAL(10, 6), elevation DECIMAL(8,2), type VARCHAR(255), volcanic_index INT(2), fatality_cause VARCHAR(255), death INT(6), death_code INT(1), injuries INT(6), injuries_code INT(1), damage DECIMAL(8, 4), damage_code INT(1), houses INT(5), houses_code INT(1))ENGINE=InnoDB")

    #################################################
    # LOAD EARTHQUAKE TABLE
    #################################################
    earthquake_values = []
    def r_listify(v):
        return v["magnitude"], v["place"], v["time"], v["timezone"], v["url"], v["tsunami"], v["id"], v["specific_type"],  v["title"], v["lng"], v["lat"], v["depth"]

    for v in earthquake_dict:
        entry_tuple = r_listify(v)
        earthquake_values.append(entry_tuple) 
    
    ## defining the Query
    query = "INSERT INTO earthquakes (magnitude, place, time, timezone, url, tsunami, id, specific_type, title, lng, lat, depth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    ## executing the query with earthquake_values
    cursor.executemany(query, earthquake_values)
    
    #country_de column: use case statement to decode title column
    cursor.execute("update earthquakes set country_de =\
      case when trim(upper(substring_index(title, ',', -1))) = 'AL' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'AK' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'AZ' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'AR' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'CA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'CO' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'CT' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'DE' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'DC' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'FL' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'GA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'HI' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'ID' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'IL' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'IN' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'IA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'KS' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'KY' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'LA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'ME' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MD' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MI' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MN' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MS' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MO' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MT' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NE' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NV' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NH' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NJ' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NM' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NY' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NC' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'ND' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'OH' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'OK' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'OR' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'PA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'RI' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'SC' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'SD' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'TN' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'TX' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'UT' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'VT' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'VA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'WA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'WV' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'WI' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'WY' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'PR' then 'United States'     \
           when trim(upper(substring_index(title, ',', -1))) = 'ALABAMA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'ALASKA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'ARIZONA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'ARKANSAS' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'CALIFORNIA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'COLORADO' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'CONNECTICUT' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'DELAWARE' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'DISTRICT OF COLUMBIA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'FLORIDA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'GEORGIA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'HAWAII' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'IDAHO' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'ILLINOIS' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'INDIANA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'IOWA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'KANSAS' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'KENTUCKY' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'LOUISIANA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MAINE' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MARYLAND' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MASSACHUSETTS' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MICHIGAN' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MINNESOTA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MISSISSIPPI' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MISSOURI' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'MONTANA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NEBRASKA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NEVADA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NEW HAMPSHIRE' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NEW JERSEY' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NEW MEXICO' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NEW YORK' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NORTH CAROLINA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'NORTH DAKOTA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'OHIO' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'OKLAHOMA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'OREGON' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'PENNSYLVANIA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'RHODE ISLAND' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'SOUTH CAROLINA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'SOUTH DAKOTA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'TENNESSEE' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'TEXAS' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'UTAH' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'VERMONT' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'VIRGINIA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'WASHINGTON' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'WEST VIRGINIA' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'WISCONSIN' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'WYOMING' then 'United States'\
           when trim(upper(substring_index(title, ',', -1))) = 'PUERTO RICO' then 'United States' \
           when trim(upper(substring_index(title, ',', -1))) = 'MX' then 'Mexico'\
           when title like '%Off the coast of Oregon%' then 'Off the coast of Oregon'\
           when title like '%Carlsberg Ridge%' then 'Carlsberg Ridge'\
           when title like '%South of the Fiji Islands%' then 'South of the Fiji Islands'\
           when title like '%Kuril Islands%' then 'Kuril Islands'\
           when title like '%Fiji region%' then 'Fiji region'  \
           when title like '%Northern Mid-Atlantic Ridge%' then 'Northern Mid-Atlantic Ridge'  \
           when title like '%Southern Mid-Atlantic Ridge%' then 'Southern Mid-Atlantic Ridge'\
           when title like '%West Chile Rise%' then 'West Chile Rise'\
           when title like '%Central Mid-Atlantic Ridge%' then 'Central Mid-Atlantic Ridge'\
           when title = 'M 3.7 - Gulf of Alaska' then 'Gulf of Alaska'\
           when title = 'M 4.0 - Banda Sea' then 'Banda Sea'\
           when title = 'M 4.2 - North Atlantic Ocean' then 'North Atlantic Ocean'\
           when title = 'M 4.3 - Western Indian-Antarctic Ridge' then 'Western Indian-Antarctic Ridge'\
           when title = 'M 4.4 - Central East Pacific Rise' then 'Central East Pacific Rise'\
           when title = 'M 4.4 - North of Svalbard' then 'North of Svalbard'\
           when title = 'M 4.4 - Off the coast of Central America' then 'Off the coast of Central America'\
           when title = 'M 4.4 - Reykjanes Ridge' then 'Reykjanes Ridge'\
           when title = 'M 4.5 - Mid-Indian Ridge' then 'Mid-Indian Ridge'\
           when title = 'M 4.5 - Southern East Pacific Rise' then 'Southern East Pacific Rise'\
           when title = 'M 4.6 - Greenland Sea' then 'Greenland Sea'\
           when title = 'M 4.6 - North of Ascension Island' then 'North of Ascension Island'\
           when title = 'M 4.6 - Northern East Pacific Rise' then 'Northern East Pacific Rise'\
           when title = 'M 4.7 - South Shetland Islands' then 'South Shetland Islands'\
           when title = 'M 4.7 - Southeast of Easter Island' then 'Southeast of Easter Island'\
           when title = 'M 4.9 - Bouvet Island region' then 'Bouvet Island region'\
           when title = 'M 5.0 - Prince Edward Islands region' then 'Prince Edward Islands region'\
           when title = 'M 5.0 - Southeast Indian Ridge' then 'Southeast Indian Ridge'\
           when title = 'M 5.0 - Vanuatu region' then 'Vanuatu region'\
           when title = 'M 5.1 - South of the Kermadec Islands' then 'South of the Kermadec Islands'\
           when title = 'M 5.2 - Pacific-Antarctic Ridge' then 'Pacific-Antarctic Ridge'\
    else trim(substring_index(title, ',', -1))\
    end")  

    ## to make final output we have to run the 'commit()' method of the database object
    db.commit()
    print(cursor.rowcount, "records inserted")

    #################################################
    # LOAD SIGNIFICANT EARTHQUAKE TABLE
    #################################################
    sig_earthquakes_df = pd.read_csv('resources/ngdc_data.tsv', sep='\t', header=0)
    # Cleans up the data and omits columns we don't need
    drop_columns = ["I_D", "FLAG_TSUNAMI", "SECOND", "EQ_MAG_MS", "EQ_MAG_MW", "EQ_MAG_MB", "EQ_MAG_ML", "EQ_MAG_MFA", "EQ_MAG_UNK", "STATE", "MISSING", "MISSING_DESCRIPTION", "INJURIES", "INJURIES_DESCRIPTION", "HOUSES_DESTROYED", "HOUSES_DESTROYED_DESCRIPTION", "HOUSES_DAMAGED", "HOUSES_DAMAGED_DESCRIPTION", "TOTAL_DEATHS_DESCRIPTION", "TOTAL_MISSING", "TOTAL_MISSING_DESCRIPTION", "TOTAL_HOUSES_DESTROYED", "TOTAL_INJURIES_DESCRIPTION", "TOTAL_HOUSES_DESTROYED_DESCRIPTION", "TOTAL_HOUSES_DAMAGED", "DAMAGE_DESCRIPTION", "REGION_CODE", "TOTAL_DAMAGE_DESCRIPTION", "DEATHS_DESCRIPTION", "TOTAL_HOUSES_DAMAGED_DESCRIPTION"]
    sig_earthquakes_df = sig_earthquakes_df.drop(drop_columns, axis = 1)
    sig_earthquakes_df = sig_earthquakes_df.rename(index=str, columns={"YEAR": "yr", "MONTH" : "month", "DAY" : "day", 'HOUR' : "hr", 'MINUTE' : "minute", 'EQ_PRIMARY' : "eq_mag_primary", "FOCAL_DEPTH": "depth", 'INTENSITY' : "intensity", 'COUNTRY' : "country", 'LOCATION_NAME' : "location_name", 'LATITUDE': "lat", 'LONGITUDE' : "lng", 'DEATHS' : "deaths", 'DAMAGE_MILLIONS_DOLLARS' : "damage_millions", 'TOTAL_DEATHS' : "total_deaths", 'TOTAL_INJURIES' : "total_injuries", 'TOTAL_DAMAGE_MILLIONS_DOLLARS' : "total_damage_millions" })
    #concatenate date/time columns and left pad with zeros so in this format: YYYY-MM-DD HH24:MI:SS
    dtg = sig_earthquakes_df['yr'].astype(str)  + '-' + \
          sig_earthquakes_df['month'].astype(str).apply(lambda x: x.zfill(2)) + '-' + \
          sig_earthquakes_df['day'].astype(str).apply(lambda x: x.zfill(2)) + ' ' + \
          sig_earthquakes_df['hr'].astype(str).apply(lambda x: x.zfill(2)) + ':' + \
          sig_earthquakes_df['minute'].astype(str).apply(lambda x: x.zfill(2)) + ':' + '00'
    #add dtg column to df
    sig_earthquakes_df['dtg'] = dtg

    # LOAD SIGNIFICANT EARTHQUAKE DATA INTO TABLE
    sig_earthquakes_df.to_sql('significant_earthquakes', con=engine, if_exists='append', index = False, index_label = "tb_id")

    print('Table EARTHQUAKES_NGDC loaded.')
    print('==============================================')
    print('*** PYTHON LOOKUP TABLE SCRIPT COMPLETED ***')
         
    cursor.execute("create table eq_filter_viz\
                    as select\
                    dtg,\
                    lat,\
                    lng,\
                    eq_mag_primary mag,\
                    depth\
                    from significant_earthquakes\
                    where `yr` >= '1900'")

    #add primary key for eq_filter_viz table                    
    cursor.execute("alter table eq_filter_viz add eq_filter_viz_pk_id int auto_increment primary key first")

    # LOAD DATA INTO PANDAS FROM CSV FILES
    df_tornadoes = pd.read_csv('resources/1950-2017_torn.csv')
    #concatenate date/time columns and left pad with zeros so in this format: YYYY-MM-DD HH24:MI:SS
    dtg = df_tornadoes['year'].astype(str)  + '-' + \
          df_tornadoes['month'].astype(str).apply(lambda x: x.zfill(2)) + '-' + \
          df_tornadoes['day'].astype(str).apply(lambda x: x.zfill(2)) + ' ' + \
          df_tornadoes['time'].astype(str).apply(lambda x: x.zfill(8))
    #add dtg column to df
    df_tornadoes['dtg'] = dtg
    df_hail = pd.read_csv('resources/1955-2017_hail.csv')
    df_wind = pd.read_csv('resources/wind.csv')
    df_tsunami = pd.read_csv('resources/tsunami.csv')
    df_volcanoes = pd.read_csv('resources/volcano.csv')

    # LOADING TORNADOES DATA INTO TABLE
    df_tornadoes.to_sql('tornadoes', con=engine, if_exists='append', index = False, index_label = "tb_id")
    # LOADING HAIL DATA INTO TABLE
    df_hail.to_sql('hail', con=engine, if_exists='append', index = False, index_label = "tb_id")
    # LOADING WIND DATA INTO TABLE
    df_wind.to_sql('wind', con=engine, if_exists='append', index = False, index_label = "tb_id")
    # LOADING TSUNAMI DATA INTO TABLE
    df_tsunami.to_sql('tsunamis', con=engine, if_exists='append', index = False, index_label = "tb_id")
    # LOADING VOLCANO DATA INTO TABLE
    df_volcanoes.to_sql('volcanoes', con=engine, if_exists='append', index = False, index_label = "tb_id")


extract_transform_load()

