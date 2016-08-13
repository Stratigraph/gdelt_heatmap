"""download and process files from gdelt to seed database"""

import datetime
from sqlalchemy import func

from model import Event, EventFile, connect_to_db, db
from sqlalchemy.orm.exc import NoResultFound
from server import app
from datetime import datetime
from bs4 import BeautifulSoup
import re
import zipfile
import requests
import os


DATADIR = "data/"
GDELT_DOWNLOAD_URL = 'http://data.gdeltproject.org/events/'
GDELT_DOWNLOAD_LIST_PAGE = 'index.html'
GDELT_DOWNLOAD_FILE_RE = r'^201\d+.*\.zip$' # only get files with dates in the 2010s

def add_zipfiles_to_db():
  """add already-downloaded files (from before I was tracking in db) to db"""

  print "GETTING FILES ALREADY DOWNLOADED"

  for filename in os.listdir(DATADIR):
    if re.match(GDELT_DOWNLOAD_FILE_RE, filename):
      try:
        file = EventFile.query.filter(EventFile.zipfile_name == filename).one()
        file.downloaded = True
        db.session.commit()

      except NoResultFound:
        file = EventFile(zipfile_name=filename, downloaded=True)
        db.session.add(file)
        print "added {} to db as downloaded".format(filename)

  db.session.commit()


def update_gdelt_stragglers():
  """ran out of disk space; db and disk got out of sync"""

  for filename in os.listdir(DATADIR):
    if re.match(GDELT_DOWNLOAD_FILE_RE, filename):
      try:
        file = EventFile.query.filter(EventFile.zipfile_name == filename).one()
        file.unzipped = False
        db.session.commit()
      except:
        print "*********couldn't find {} in db".format(filename)


def get_gdelt_files():
  """get list of gdelt files from gdelt download site, add to gdelt_files table"""

  # get file list
  print "getting file list"

  r = requests.get(GDELT_DOWNLOAD_URL + GDELT_DOWNLOAD_LIST_PAGE)

  soup = BeautifulSoup(r.content, 'html.parser')
  links = soup.find_all('a')

  for link in links:
    link_text = link.get_text()

    if re.match(GDELT_DOWNLOAD_FILE_RE, link_text):
      try:
        file = EventFile.query.filter(EventFile.zipfile_name == link_text).one()
        print "{} already in db. Skipping.".format(link_text)

      except NoResultFound: 
        file = EventFile(zipfile_name=link_text)
        db.session.add(file)

  db.session.commit()


def process_gdelt_files():
  """download, unzip, and process files, one at a time (for the disk space!)"""

  # because of disk space issues, process unzipped files first
  for file in EventFile.query.filter(EventFile.unzipped == True).all():
    if not file.processed:
      add_to_db(file)


  # now process the rest
  for file in EventFile.query.filter(EventFile.unzipped == False).all():
    if not file.downloaded:
      download_gdelt_file(file)
    if not file.unzipped:
      uznip_gdelt_file(file)
    if not file.processed:
      add_to_db(file)


def download_gdelt_file(file):
  """download each file in the gdelt_files table"""

  name = file.zipfile_name

  print "downloading", name

  filepath = DATADIR + name
  r = requests.get(GDELT_DOWNLOAD_URL + name)

  # write to file
  with open(filepath, "wb") as code:
    code.write(r.content)

  file.downloaded = True

  # commit here instead of end of function, in case script gets interrupted
  db.session.commit()
  

def unzip_gdelt_file(file):
    """unzip each .zip file in the data dir"""

    name = file.zipfile_name

    print "unzipping", name

    filepath = DATADIR + name

    # unzip the file
    zip_ref = zipfile.ZipFile(filepath, 'r')
    zip_contents = zip_ref.namelist()

    # if there's more (or less) than one file, we're in trouble
    if len(zip_contents) != 1:
      print "***************{} contains {} archives. Skipping.".format(filepath, len(zip_contents))
      return

    zip_ref.extractall(DATADIR)
    zip_ref.close()

    # rm the zip file for disk space
    try:
      os.remove(DATADIR + name)
    except:
      print "*********could not remove file {}".format(name)

    # we've already checked that there's only one file
    file.csvfile_name = zip_contents[0]
    file.unzipped = True

    # commit here instead of end of function, in case script gets interrupted
    db.session.commit()


def add_to_db(file):
    """parse file contents for file param and add data to db"""
    
    # indexes taken from these files: 
    # http://gdeltproject.org/data/lookups/CSV.header.dailyupdates.txt
    # http://gdeltproject.org/data/lookups/CSV.header.historical.txt

    # reference: 
    # http://data.gdeltproject.org/documentation/GDELT-Data_Format_Codebook.pdf

    filepath = DATADIR + file.csvfile_name
    print "processing", filepath

    # process line by line
    with open(filepath) as f:
      for line in f:
        process_line(line)

    file.processed = True
    db.session.commit()

    # rm the csv file for disk space
    try:
      os.remove(filepath)
    except:
      print "*********could not remove file {}".format(filepath)


def process_line(line):
  """add an event based on a gdelt file line"""

  tokens = line.split('\t')

  # the spec changed April 1, 2013, but it didn't affect any of these 
  # fields
  eid = tokens[0]
  date = datetime.strptime(tokens[1], '%Y%m%d')
  ecode = tokens[26]
  try:
    # don't fall over if one of these isn't populated; just move on
    goldstein = float(tokens[30])
    num_mentions = int(tokens[31])
    lat = float(tokens[53])
    lng = float(tokens[54])
  except:
    return

  evt = Event(gdelt_id=eid, 
              event_date=date, 
              event_code=ecode, 
              goldstein=goldstein,
              num_mentions=num_mentions,
              lat=lat,
              lng=lng)

  db.session.add(evt)

if __name__ == "__main__":
    connect_to_db(app)

    # create tables if they don't exist
    db.create_all()

    # print "*"*10, "GETTING FILE LIST"
    # get_gdelt_files()

    print "*"*10, "PROCESSING FILES"
    process_gdelt_files()
