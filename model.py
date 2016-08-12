"""Models and database functions for Ratings project."""
import time
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

class Event(db.Model):

  __tablename__ = "events"

  gdelt_id = db.Column(db.Integer, primary_key=True)
  event_date = db.Column(db.DateTime)
  event_code = db.Column(db.String(8))
  goldstein = db.Column(db.Float)
  num_mentions = db.Column(db.Integer)
  lat = db.Column(db.Float)
  lng = db.Column(db.Float)



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gdelt'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
