"""functions involving the database"""

from model import db, Event
from sqlalchemy import extract


def get_events():
  """return all events in db for a particular year and week"""
  
  return Event.query.all()
