import datetime
from sqlalchemy import func

from model import Event, connect_to_db, db
from server import app
from datetime import datetime
from bs4 import BeautifulSoup
import re
import zipfile
import requests


DATADIR = "data/"
GDELT_DOWNLOAD_URL = 'http://data.gdeltproject.org/events/'
GDELT_DOWNLOAD_LIST_PAGE = 'index.html'
GDELT_DOWNLOAD_FILE_RE = r'^201\d+.*\.zip$' # only get files with dates in the 2010s

def get_gdelt_files():
  """get list of gdelt files from gdelt download site, return list"""

  # get file list
  print "getting file list"

  r = requests.get(GDELT_DOWNLOAD_URL + GDELT_DOWNLOAD_LIST_PAGE)

  soup = BeautifulSoup(r.content, 'html.parser')
  links = soup.find_all('a')

  relevant_link_list = []

  for link in links:
    link_text = link.get_text()
    if re.match(GDELT_DOWNLOAD_FILE_RE, link_text):
      relevant_link_list.append(link_text)

  return relevant_link_list

def process_gdelt_files(file_list):
  """download and unzip each file in the argument list, and add contents to the db"""

  # download and unzip each file
  for name in file_list:
    print "downloading", name

    r = requests.get(GDELT_DOWNLOAD_URL + name)

    filepath = DATADIR + name

    # write to file
    with open(filepath, "wb") as code:
      code.write(r.content)

    # unzip the file
    zip_ref = zipfile.ZipFile(filepath, 'r')
    zip_contents = zip_ref.namelist()

    # if there's more than one file, we're in trouble
    if len(zip_contents) != 1:
      print "***************{} contains {} archives. Skipping.".format(filepath, len(zip_contents))
      continue

    zip_ref.extractall(DATADIR)
    zip_ref.close()

    # we've already checked that there's only one file
    unzipped_filepath = zip_contents[0]

    # open the file and add the contents to the db
    add_to_db(DATADIR + unzipped_filepath)


def add_to_db(filepath):
    """parse file contents and add data to db"""
    
    # indexes taken from these files: 
    # http://gdeltproject.org/data/lookups/CSV.header.dailyupdates.txt
    # http://gdeltproject.org/data/lookups/CSV.header.historical.txt

    # reference: 
    # http://data.gdeltproject.org/documentation/GDELT-Data_Format_Codebook.pdf
    print "processing", filepath
    num_notprocessed = 0
    num_processed = 0

    with open(filepath) as f:
      for line in f:
        tokens = line.split('\t')

        # for i, token in enumerate(tokens):
        #   print i, token

        # exit()

        # the spec changed April 1, 2013, but it didn't affect any of these 
        # fields
        eid = tokens[0]
        date = datetime.strptime(tokens[1], '%Y%m%d')
        ecode = tokens[26]
        goldstein = float(tokens[30])
        num_mentions = int(tokens[31])
        try:
          lat = float(tokens[53])
          lng = float(tokens[54])
          num_processed += 1
        except:
          num_notprocessed += 1
          continue

        evt = Event(gdelt_id=eid, 
                    event_date=date, 
                    event_code=ecode, 
                    goldstein=goldstein,
                    num_mentions=num_mentions,
                    lat=lat,
                    lng=lng)

        db.session.add(evt)

    db.session.commit()
    print "finished processing {}. Processed lines: {} Not processed lines: {}\n".format(filepath, num_processed, num_notprocessed)


if __name__ == "__main__":
    connect_to_db(app)

    # start with a clean slate
    db.drop_all()
    db.create_all()

    # files_to_download = get_gdelt_files()
    # process_gdelt_files(files_to_download)


    add_to_db('data/20160811.export.CSV')

    db.session.commit()
