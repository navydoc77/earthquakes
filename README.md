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

Modules required:
mysql-connector
mysql
flask_sqlalchemy

Start database before running etl.py


## To run:

Run app.py at terminal line

Routes:
<strong>@app.route("/")</strong>
<p>-renders homepage

<strong>@app.route("/magnitudes")</strong>
<p>-access usgs earthquake data
<p>-returns a list of unique earthquakes by magnitude

<strong>@app.route("/earthquakes", methods=['GET'])</strong>
<p>-access usgs earthquake data
<p>-returns a json of all earthquake events and corresponding data

<strong>@app.route("/significant_earthquakes", methods=['GET'])</strong>
<p>-access signficant earthquake data from csv file</p>
<p>-returns a json of all significant earthquake events</p>

<strong>@app.route("/hail", methods=['GET'])</strong>
<p>-access signficant hail data from csv file
<p>-returns a json of all significant hail events

<strong>@app.route("/wind", methods=['GET'])</strong>
<p>-access signficant wind data from csv file
<p>-returns a json of all significant wind events

<strong>@app.route("/tsunamis", methods=['GET'])</strong>
<p>-access signficant tsunamis data from csv file
<p>-returns a json of all significant tsunamis events

<strong>@app.route("/volcanoes", methods=['GET'])</strong>
<p>-access signficant volcanoes data from csv file
<p>-returns a json of all significant volcanoes events

### Load data by doing:

Run etl.py at terminal line
-This extracts the data from api and csv files.
-A mysqyl database is created
-Data is loaded into mysqual

Note that for iOS, in the `config.py` file you will have to use `engine = create_engine('mysql+pymysql://root:root@localhost')`

### Run application by performing the following:

Run app.py at terminal line
-routes