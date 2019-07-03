import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import or_

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import db_conn

app = Flask(__name__)

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


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/data.sqlite"
db = SQLAlchemy(app)

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(db.engine, reflect=True)

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

if __name__ == "__main__":
    app.run()