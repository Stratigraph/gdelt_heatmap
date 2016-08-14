"""helper functions for server.py"""

from db_functions import get_events

def get_event_data(year, week):
    """returns dict of event info for this week and year"""

    # returns list of event objects for this week and year
    events = get_events(year, week)

    # to store data as collected
    events_data = {}

    for event in events:
        # round lat and long, so as to cluster similar events together

        lat = int(event.lat)
        lng = int(event.lng)

        # key can't be a tuple for jsonification, so using string
        latlng = '|'.join([str(lat), str(lng)])

        if latlng not in events_data:
            events_data[latlng] = {'lat': lat, 'lng': lng, 'evts': []}

        # add title, url, and event code (type) info  
        evt_info = {'title': event.title, 'url': event.url, 'code': event.event_code}
        events_data[latlng]['evts'].append(evt_info)

    return events_data
