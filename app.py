import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session from Python to the DB
session = Session(engine)

#################################################
# Set up Flask and landing page
#################################################
app = Flask(__name__)

# last 12 months variable
begin_date = '2016-08-23'
end_date = '2017-08-23'
@app.route("/")
def welcome():
    return (
        f"<p>Welcome to Jordon's Hawaii Measurement</p>"
        f"<p>Usage:</p>"
        f"/api/v1.0/precipitation<br/>Returns a JSON list of percipitation data for ALL dates<br/><br/>"
        f"/api/v1.0/stations<br/>Returns a JSON list of stations<br/><br/>"
        f"/api/v1.0/tobs<br/>Returns a JSON list of the TOBS of Previous Year<br/><br/>"
        f"/api/v1.0/start<br/>Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date<br/><br/>."
        f"/api/v1.0/start/end<br/>Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range<br/><br/>."
    )

# /api/v1.0/precipitation
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value..
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_query = session.query(Measurement.date, func.avg(Measurement.prcp)).group_by(Measurement.date).all()
    return jsonify(prcp_query)


# /api/v1.0/stations
# Return a JSON list of stations.
@app.route("/api/v1.0/stations")
def stations():
    station_query = session.query(Station.station, Station.name).all()
    return jsonify(station_query)


# /api/v1.0/tobs
# Returns a JSON list of the TOBS of Previous Year
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_query = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= begin_date).all()
    return jsonify(tobs_query)


# /api/v1.0/<start>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    temp_start_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2010-06-10').all()
    return jsonify(temp_start_query)


# /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    temp_startend_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= begin_date).filter(Measurement.date <= end_date).all()
    return jsonify(temp_startend_query)

if __name__ == "__main__":
    app.run(debug=True)