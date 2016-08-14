"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db
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

    return render_template("map_google.html", gmaps_key=GMAPS_KEY)

@app.route('/d3')
def render_d3():

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
