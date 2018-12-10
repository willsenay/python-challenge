import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Precipitation Setup
#################################################

# set which columns to select into a list
sel = [Measurement.date, 
       Measurement.prcp] 

# select the columns and filter the date. then order the data
prcp_data = session.query(*sel).\
    filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2016-08-23').\
    order_by(Measurement.date).all()

# create the dictionary
prcp_dict = {}
for i in prcp_data:
    prcp_dict[i[0]] = i[1]

#################################################
# Station Setup
#################################################

# select the list of stations
station_list= session.query(Station.station).all()

#################################################
# Tobs Setup
#################################################

# set which columns to select into a list
sel = [Measurement.date, 
       Measurement.tobs] 

# select the columns and filter the date. then order the data
tobs_data = session.query(*sel).\
    filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2016-08-23').\
    order_by(Measurement.date).all()

# create the dictionary
tobs_dict = {}
for i in tobs_data:
    tobs_dict[i[0]] = i[1]

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return(
        '<div class="container">'
        '    <!-- Row 1 -->'
        '    <div class="row">'
        '      <div class="col-md-12">'
        '        <h1>Possible url endings:</h1>'
        '      </div>'
        '    </div>'
        '    <!-- Row 2 -->'
        '    <div class="row">'
        '      <div class="col-md-12">'
        '        <p style="text-indent :5em;">"/api/v1.0/precipitation" : Returns'
        '            dates and precipitation</p>'
        '      </div>'
        '    </div>'
        '    <!-- Row 2 -->'
        '    <div class="row">'
        '      <div class="col-md-12">'
        '        <p style="text-indent :5em;">"/api/v1.0/stations" : Returns'
        '            list of stations</p>'
        '      </div>'
        '    </div>'
        '    <!-- Row 3 -->'
        '    <div class="row">'
        '      <div class="col-md-12">'
        '        <p style="text-indent :5em;">"/api/v1.0/tobs" : Returns'
        '            list of Temperature Observations (tobs) '
        '            for the previous year</p>'
        '      </div>'
        '    </div>'
        '    <!-- Row 4 -->'
        '    <div class="row">'
        '      <div class="col-md-12">'
        '        <p style="text-indent :5em;">"/api/v1.0/(start)" : Returns '
        '              list of the minimum temperature, average temperature, '
        '              and max temperature for a given start date</p>'
        '      </div>'
        '    </div>'
        '    <!-- Row 5 -->'
        '    <div class="row">'
        '      <div class="col-md-12">'
        '        <p style="text-indent :5em;">"/api/v1.0/(start)/(end)" : Returns '
        '              list of the minimum temperature, average temperature, '
        '              and max temperature for a given start/end date range</p>'
        '      </div>'
        '    </div>'
        '</div>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    return jsonify(prcp_dict)

@app.route('/api/v1.0/stations')
def stations():
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    return jsonify(tobs_dict)

@app.route('/api/v1.0/<start>')
def start(start):
    
    # set select to min, max, and avg
    sel = [func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]

    # select from dates that are greater than or equal to entered date
    temp_describe = session.query(*sel).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= start).\
        order_by(Measurement.date).all()

    # set up dictionary to jsonify
    temp_list = np.array(temp_describe).ravel()
    temp_dict = {}
    temp_dict['TMIN'] = temp_list[0]
    temp_dict['TMAX'] = temp_list[1]
    temp_dict['TAVG'] = temp_list[2]
    
    # return json
    return jsonify(temp_dict)

@app.route('/api/v1.0/<start>/<end>')
def end(start, end):

    # set select to min, max, and avg
    sel = [func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]

    # select from dates that between the entered dates
    temp_describe = session.query(*sel).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= start).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= end).\
        order_by(Measurement.date).all()

    # set up dictionary to jsonify
    temp_list = np.array(temp_describe).ravel()
    temp_dict = {}
    temp_dict['TMIN'] = temp_list[0]
    temp_dict['TMAX'] = temp_list[1]
    temp_dict['TAVG'] = temp_list[2]
    
    # return json
    return jsonify(temp_dict)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
