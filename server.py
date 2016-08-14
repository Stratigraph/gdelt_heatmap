"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Event

from helper import get_event_data

import os


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "v9m2hY7#%z!dWar8bMW^"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# keep secret key out of git
GMAPS_KEY = os.environ['GOOGLE_MAPS_API_KEY']


@app.route('/')
def index():
    """Homepage."""

    return render_template("home.html")


@app.route('/google')
def render_google():
    """render a google map with the data"""

    return render_template("map_google.html", gmaps_key=GMAPS_KEY)

@app.route('/events.json')
def return_events_json():
    """return events json for google mapping"""

    year = request.args.get('year', 2016)
    week = request.args.get('week', 31)

    # returns list of event objects for this week and year
    events_data = get_event_data(year, week)

    return jsonify(events_data)


@app.route('/d3')
def render_d3():
    """render a d3 map with the data"""

    return render_template("map_d3.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5005)
