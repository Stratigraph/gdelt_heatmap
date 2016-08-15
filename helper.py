"""helper functions for server.py"""

from db_functions import get_events

def get_event_data():
    """returns dict of event info from the db"""

    # returns list of event objects from the db
    events = get_events()

    # to store data as collected
    events_data = {}

    for event in events:
        # sort by date
        edate = event.event_date

        # get unix timestamp
        date_key = edate.strftime('%s')

        if date_key not in events_data:
            events_data[date_key] = {}

        # round lat and long, so as to cluster similar events together

        lat = int(event.lat)
        lng = int(event.lng)

        # key can't be a tuple for jsonification, so using string
        latlng = '|'.join([str(lat), str(lng)])

        if latlng not in events_data[date_key]:
            events_data[date_key][latlng] = {'lat': lat, 'lng': lng, 'apEvts': [], 'fgEvts': []}

        # add title, url, and event code (type) info  
        evt_info = {'title': event.title, 'url': event.url}

        if event.event_code == '055': # apology:
            elist = 'apEvts'
        elif event.event_code == '056': # forgiveness
            elist = 'fgEvts'
        else:
            print "bad event code: ", event_code
            continue

        events_data[date_key][latlng][elist].append(evt_info)

    # do a little work here to get min and max dates, to avoid JS messiness
    sort_keys = sorted(events_data.keys())
    
    response = {'min': sort_keys[0],
                'max': sort_keys[-1],
                'events': events_data}

    return response
