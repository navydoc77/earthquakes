# Natural Disasters
![Earth Hackers!](resources/disaster_collage_funny.jpg "Earth Hackers!")
---

This application is designed to be educational and provide information, data, and graphics for natural disasters.

## Data Source

The data used in this application was ingested from:
<li><a href="https://www.ngdc.noaa.gov/nndc/struts/form?t=101650&s=1&d=1" target="_blank">National Geophysical Data Center</a></li>
<li><a href="https://earthquake.usgs.gov/earthquakes/feed/" target="_blank">United States Geological Survey</a></li>


## Requirements:

Flask ... etc etc

## To run:

### Load data by doing:

Run etl.py at terminal line
-This extracts the data from api and csv files.
-A mysqyl database is created
-Data is loaded into mysqual

Note that for iOS, in the `config.py` file you will have to use `engine = create_engine('mysql+pymysql://root:root@localhost')`

### Run application by performing the following:

Run app.py at terminal line
-routes