import datetime
from sqlalchemy import func

from model import Event, connect_to_db, db
from server import app
from datetime import datetime
from bs4 import BeautifulSoup
import re
import zipfile


DATADIR = "/data/"
GDELT_DOWNLOAD_URL = 'http://data.gdeltproject.org/events/'
GDELT_DOWNLOAD_LIST_PAGE = 'index.html'
GDELT_DOWNLOAD_FILE_RE = r'^20\d+.*\.zip$' # only get files with dates in the 2000s

def add_gdelt_data():

  # get file list
  r = requests.get(GDELT_DOWNLOAD_URL + GDELT_DOWNLOAD_LIST_PAGE)

  soup = BeautifulSoup(r.content, 'html.parser')
  links = soup.find_all('a')

  relevant_link_list = []

  for link in links:
    link_text = link.get_text()
    if re.match(GDELT_DOWNLOAD_FILE_RE, link_text):
      relevant_link_list.append(link_text)

  # download and unzip each file
  for name in relevant_link_list:

    r = requests.get(GDELT_DOWNLOAD_URL + name)

    filepath = DATADIR + name

    # write to file
    with open(filepath, "wb") as code:
      code.write(r.content)

    # unzip the file
    zip_ref = zipfile.ZipFile(filepath, 'r')
    unzipped_filepath = zip_ref.extractall(DATADIR)
    zip_ref.close()

    # open the file and add the contents to the db
    # indexes taken from this file: 
    # http://data.gdeltproject.org/documentation/GDELT-Data_Format_Codebook.pdf
    print "processing", unzipped_filepath
    
    with open(unzipped_filepath) as f:
      for line in f:
        tokens = line.split('\t')
        eid = tokens[0]
        date = datetime.strptime(tokens[1], '%Y%m%d')
        ecode = tokens[16]
        goldstein = tokens[20]
        num_mentions = tokens[21]
        lat = tokens[30]
        lng = tokens[31]

        evt = Event(event_id=eid, 
                    event_date=date, 
                    event_code=ecode, 
                    goldstein=goldstein,
                    num_mentions=num_mentions,
                    lat=lat,
                    lng=lng)

        db.session.add(evt)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # start with a clean slate
    db.drop_all()
    db.create_all()

    add_gdelt_data()

    db.session.commit()
