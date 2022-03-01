#Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np
import datetime as dt

# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Create our session (link) from Python to the DB
session = Session(engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Find the most recent date in the data set.
first_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Starting from the most recent data point in the database, calculate the date one year from the last date in data set.
query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

session.close()
#Setup App
app = Flask(__name__)

# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes in the Hawaii Database:<br/>"
        f"Homepage: "
        f"/<br/>"
        f"Precipitation readings for a given date: "
        f"/api/v1.0/precipitation<br/>"
        f"List of stations: "
        f"/api/v1.0/stations<br/>"
        f"Dates and temperatures for most active station: "
        f"/api/v1.0/tobs"
        f"Summary statistics for a given start or start-end range: "
        f"/api/v1.0/<start>` and `/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    #Create session using engine
    session = Session(engine)
    #Query, pass to list, and jsonify
    data = session.query(Measurement.date, Measurement.prcp).all()
    precip_list = []
    for date, prcp in data:
        pdict = {}
        pdict["date"] = date
        pdict["prcp"] = prcp
        
        precip_list.append(pdict)
    session.close()
    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset.

if __name__ == "__main__":
    app.run(debug=True)