"""Models and database functions for heatmaps project."""
import time
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

class Event(db.Model):
  """gdelt events and their data"""

  __tablename__ = "events"

  gdelt_id = db.Column(db.Integer, primary_key=True)
  event_date = db.Column(db.DateTime)
  event_code = db.Column(db.String(8))
  goldstein = db.Column(db.Float)
  num_mentions = db.Column(db.Integer)
  lat = db.Column(db.Float)
  lng = db.Column(db.Float)

  def __repr__(self):
    """Provide helpful representation when printed."""

    return "<Event gdelt_id={} event_date={}>".format(self.gdelt_id, 
                                                      self.event_date)


class EventFile(db.Model):
  """downloaded files from gdelt"""

  __tablename__ = "gdelt_files"

  file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  zipfile_name = db.Column(db.String(64), nullable=False)
  csvfile_name = db.Column(db.String(64))

  # track whether the file has been downloaded
  downloaded = db.Column(db.Boolean, default=False)

  # track whether the file has been unzipped
  unzipped = db.Column(db.Boolean, default=False)

  # track whether the data has been entered into the db
  processed = db.Column(db.Boolean, default=False)


  def __repr__(self):
    """Provide helpful representation when printed."""

    repr_string = "<EventFile file_id={} ".format(self.file_id)
    repr_string += "zipfile_name={} ".format(self.zipfile_name)
    repr_string += "downloaded={} ".format(self.downloaded)
    repr_string += "unzipped={} ".format(self.unzipped)
    repr_string += "processed={}>".format(self.processed)

    return repr_string


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
