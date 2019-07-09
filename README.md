# Natural Disasters
![Earth Hackers!](resources/disaster_collage_funny.jpg "Earth Hackers!")

This application is designed to be educational and provide information, data, and graphics for natural disasters.  You can view the application by clicking on this link: <a href="https://natural-disaster-app.herokuapp.com/" target="_blank">Natural Disasters</a>

If you want to install the application on your device, see **ETL/Run the Application Procedure** below.

### Repository Contents

- [etl.py](etl.py)  This contains the extract, transform, and load logic for the database.
- [db_conn.py](db_conn.py)  This uses sqlalchemy for database connection, engine creation, reflection, and session logic.
- [app.py](app.py)  This will run the natural disasters application.

## Requirements 

See [Requirements.txt](Requirements.txt) file.  Ensure these requirements are satisifed on your local device before performing the ETL steps below.


## ETL/Run the Application Procedure

### Step 1:

- In the application folder, create a **.env** file by typing the following:
 
```
$ touch .env
```

### Step 2:

- Edit the .env file.  See below as an example of the .env file contents.

```
# Example Database Connection
# Replace with your own values for deployment
DATABASE_DIALECT=mysql
DATABASE_USERNAME=your_username
DATABASE_PASSWORD=your_password
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
DATABASE_NAME=natural_disasterdb
``` 

### Step 3:

- At the command line, run the following command:
``` 
$ python etl.py 
```

This will build the MySQL database and load the tables. 

### Step 4:
- Within the application folder, type the following at the command line:

```
$ python app.py
```

### Step 5:
- Open a web browser and for the url type: ``127.0.0.1:5000``.  You can now view the application.

## Data Sources

The data used in this application was ingested from:
- [United States Geological Survey](https://earthquake.usgs.gov/earthquakes/feed/)
- [National Centers for Environmental Information](https://www.ngdc.noaa.gov/ngdcinfo/onlineaccess.html)
