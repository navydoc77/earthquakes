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

Run app.py at terminal line

Routes:
@app.route("/")
-renders homepage

@app.route("/magnitudes")
-access usgs earthquake data
-returns a list of unique earthquakes by magnitude

@app.route("/earthquakes", methods=['GET'])
-access usgs earthquake data
-returns a json of all earthquake events and corresponding data

@app.route("/significant_earthquakes", methods=['GET'])
<p>-access signficant earthquake data from csv file</p>
<p>-returns a json of all significant earthquake events</p>

@app.route("/hail", methods=['GET'])
-access signficant hail data from csv file
-returns a json of all significant hail events

@app.route("/wind", methods=['GET'])
-access signficant wind data from csv file
-returns a json of all significant wind events

@app.route("/tsunamis", methods=['GET'])
-access signficant tsunamis data from csv file
-returns a json of all significant tsunamis events

@app.route("/volcanoes", methods=['GET'])
-access signficant volcanoes data from csv file
-returns a json of all significant volcanoes events

### Load data by doing:

Run ETL.py at terminal line

Note that for iOS, in the `config.py` file you will have to use `engine = create_engine('mysql+pymysql://root:root@localhost')`

### Run application by performing the following:
