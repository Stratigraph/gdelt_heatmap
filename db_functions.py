"""functions involving the database"""

from model import db, Event
from sqlalchemy import extract


def get_events(year, week):
  """return all events in db for a particular year and week"""
  query = Event.query
  query.filter(extract('week', Event.event_date) == week)
  query.filter(extract('year', Event.event_date) == year)

  return query.all()