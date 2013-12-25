"""Module for handling flights' part of the API"""

import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from domain.constants import API_BASE
from domain.general import send_post, get

BASE = API_BASE + "availability/flights/"

def get_roundtrip_flight(adults="1", children="0", infants="0",
                         cabintype="ECONOMY", stops="MORE_THAN_ONE", **kwargs):
    """Return info on roundtrip flights
    
    Required arguments:
    orig: 3-letter code for airport or city of origin
    to: 3-letter code for airport or city of destination
    departure: yyyy-mm-dd date of departure
    returning: yyyy-mm-dd date of return
    
    Optional arguments:
    adults: quantity of adults travelling
    children: quantity of children travelling
    infants: quantity of infants travelling
    cabintype: cabin type preference (ECONOMY, BUSINESS, FIRSTCLASS, 
                        PREMIUM_ECONOMY, PREMIUM_BUSINESS, PREMIUM_FIRSTCLASS)
    stopsadvancedparameter: how many stops (NONE, ONE, MORE_THAN_ONE)
    
    Return value is subject to change. Right now it's a dict cointaining:
    result['flights']: raw info on flights
    result['matrix']: condensed summary to build the matrix as seen in
                        despegar.com's main search page.
    """
    required_args = ['orig', 'to', 'departure', 'returning']
    for arg in required_args:
        if arg not in kwargs:
            raise TypeError("Missed a required argument. Required arguments "
                "are: " + ", ".join(required_args))
    content = get(BASE + "roundTrip" + "/" + kwargs['orig'] + "/" +
                  kwargs['to'] + "/" + kwargs['departure'] + "/" +
                  kwargs['returning'] + "/" + adults + "/" + children + "/" +
                  infants + "?cabintype=" + cabintype +
                  "&stopsadvancedparameter=" + stops)
    result = {}
    if 'flights' in content:
        result['flights'] = content['flights']
    if 'meta' in content:
        if 'summaryMatrix' in content['meta']:
            result['matrix'] = content['meta']['summaryMatrix']
    return result

def get_mult_flights(adults="1", children="0", infants="0",
                         cabintype="ECONOMY", stops="MORE_THAN_ONE", **kwargs):
    """Return info on multiple flights
    
    Required arguments:
    orig: comma-separated list of 3-letter code for airport or city of origin
    to: comma-separated list of 3-letter code for airport or city of destination
    departure: comma-separated list of yyyy-mm-dd dates of departure
    
    The rest of the information required/returned is the same as
    get_roundtrip_flight. Required arguments for this function must have commas
    in them, so that despegar.com can match, e.g.:
    - flight from orig[0] to to[0] on departure[0]
    - flight from orig[1] to to[0] on departure[1]
    """
    required_args = ['orig', 'to', 'departure']
    for arg in required_args:
        if arg not in kwargs:
            raise TypeError("Missed a required argument. Required arguments "
                "are: " + ", ".join(required_args))
        if kwargs[arg].find(',') == -1:
            raise TypeError("Arguments in this function must have commas!")
    
    content = get(BASE + "multipleDestinations" + "/" + kwargs['orig'] + "/" +
                kwargs['to'] + "/" + kwargs['departure'] + "/" + adults + "/" +
                children + "/" + infants + "?cabintype=" + cabintype +
                "&stopsadvancedparameter=" + stops)
    result = {}
    if 'flights' in content:
        result['flights'] = content['flights']
        for item in result['flights']:
            # Copy each flight's 'id' to its root so we can work it as usual
            item['id'] = item['itineraryInfo']['id']
    if 'meta' in content:
        if 'summaryMatrix' in content['meta']:
            result['matrix'] = content['meta']['summaryMatrix']
    return result

def get_best_flights(flights_raw):
    """Return best flights data
    
    Required arguments:
    flights_raw: a dict containing two elements, as returned by
                    get_roundtrip_flight
    
    Returns a list of the best flights for each airline
    """
    ids = []
    for item in flights_raw['matrix']:
        for id in iter(item['clustersByStops'].values()):
            if id is not None:
                # Needed not to break when despegar.com returns IDs in the
                # matrix that are not in the raw data.
                if id in [flight['id'] for flight in flights_raw['flights'] if flight['id'] == id]:
                    ids.append(id)
    best_flights = []
    for id in ids:
        best_flights.append(
            [flight for flight in flights_raw['flights'] if flight['id'] == id][0])
    return best_flights

def get_flights_summary(best_flights):
    
    """
    Return a summary of the best flights available
    
    Required arguments:
    best_flights: a list of dicts as returned by get_best_flights
    
    Returns a list of select field from best_flights
    """
    summary = []
    for flight in best_flights:
        summary_flight = {}
        summary_flight['id'] = flight['id']
        summary_flight['price'] = flight['priceInfo']['total']['fare']
        routes = []
        routekeys = ['outboundRoutes', 'inboundRoutes', 'routes']
        for key in routekeys:
            if key in flight.keys():
                for item in flight[key]:
                    if item['type'] == 'AIR':
                        route = {}
                        route['duration'] = item['duration']
                        route['changes_airport'] = item['hasAirportChange']
                        route['segments'] = []
                        for seg_ in item['segments']:
                            segment = {}
                            segment['departure'] = {}
                            segment['arrival'] = {}
                            segment['departure']['airport']= seg_['departure']['locationDescription']
                            segment['departure']['date']= seg_['departure']['date']
                            segment['departure']['timezone']= seg_['departure']['timezone']
                            segment['arrival']['airport']= seg_['arrival']['locationDescription']
                            segment['arrival']['date']= seg_['arrival']['date']
                            segment['arrival']['timezone']= seg_['arrival']['timezone']
                            segment['type'] = seg_['marketingCabinTypeCode']
                            segment['duration'] = seg_['duration']
                            segment['carrier'] = seg_['marketingCarrierDescription']
                            segment['actual_carrier'] = seg_['operatingCarrierDescription']
                            segment['code'] = seg_['operatingCarrierCode']
                            route['segments'].append(segment)
                        routes.append(route)
        #summary_flight['routes'] = sorted(routes, key=lambda item: item['segments']['departure']['date'])
        summary_flight['routes'] = routes
        summary.append(summary_flight)
    # Return summary, sorted by price
    return sorted(summary,  key=lambda item: item['price'])


def cheapest_roundtrip_flight(**kwargs):
    """Find out for a given start date and duration, origin and destination, the
    best flights available in a given timespan (e.g. 90 days after start date).
    
    This mimics despegar.com's 'Find best flight', which typically has a 60-90
    days' timespan. We make it configurable and query the API in
    a threaded way so as to be more efficient.
    
    Required arguments:
    orig: 3-letter code for airport or city of origin
    to: 3-letter code for airport or city of destination
    start_date: yyyy-mm-dd date of departure
    duration: an integer determining how many days are between start_date and
        end_date (we don't ask you for end_date as it will be calculated
    timespan: an integer determining how many days after start_date you wish
        to query with the same values (duration of your trip, origin and
        destination)
    """
    
    required_args = ['start_date', 'duration', 'timespan', 'orig', 'to']
    for arg in required_args:
        if arg not in kwargs:
            raise TypeError("Missed a required argument. Required arguments "
                "are: " + ", ".join(required_args))
    
    duration = kwargs['duration']
    timespan = kwargs['timespan']
    start_date = datetime.datetime.strptime(kwargs['start_date'], '%Y-%m-%d').date()
    end_date = start_date + datetime.timedelta(days=duration)
    orig = kwargs['orig']
    to = kwargs['to']
    
    target_args = []
    
    for diff in range(timespan):
        start = (start_date + datetime.timedelta(days=diff)).strftime('%Y-%m-%d')
        end = (end_date + datetime.timedelta(days=diff)).strftime('%Y-%m-%d')
        kw = {}
        kw['orig'] = orig
        kw['to'] = to
        kw['departure'] = start
        kw['returning'] = end
        target_args.append(kw)
    
    return cheapest_flights_caller(0, target_args)

def cheapest_mult_flight(**kwargs):
    """Same as cheapest_roundtrip_flight but for multiple destinations.
    
    Instead of start_date and duration, a single argument 'departures' must be
    provided, alongside orig, to and timespan. Sans timespan, all the others
    must have the same amount of commas in them.
    """
    
    required_args = ['departures', 'timespan', 'orig', 'to']
    for arg in required_args:
        if arg not in kwargs:
            raise TypeError("Missed a required argument. Required arguments "
                "are: " + ", ".join(required_args))
        if arg != 'timespan':
            if kwargs[arg].find(',') == -1:
                raise TypeError("Arguments in this function must have commas!")
        else:
            if type(kwargs[arg]) != type(1):
                raise TypeError("Timespan must be an integer!")
    
    timespan = kwargs['timespan']
    int_start_dates = [datetime.datetime.strptime(target_date, '%Y-%m-%d').date() 
                       for target_date in kwargs['departures'].split(',')]
    target_args = []
    orig = kwargs['orig']
    to = kwargs['to']

    
    for diff in range(timespan):
        departure = ','.join(
                    [(target_date + datetime.timedelta(days=diff)).
                     strftime('%Y-%m-%d') for target_date in int_start_dates])
        kw = {}
        kw['orig'] = orig
        kw['to'] = to
        kw['departure'] = departure
        target_args.append(kw)
    
    return cheapest_flights_caller(1, target_args)

def cheapest_flights_caller(mult, target_args):
    """Caller for both cheapest_roundtrip_flight and cheapest_mult_flight"""
    
    cheapest_flights = {}
    if mult == 0:
        fn = get_roundtrip_flight
    elif mult == 1:
        fn = get_mult_flights

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_data = {executor.submit(fn, **kw): kw for kw in target_args}
        for future in as_completed(future_to_data):
            kw = future_to_data[future]
            flights_raw = future.result()
            best_flights = get_best_flights(flights_raw)
            summary = get_flights_summary(best_flights)
            best_flight = summary[0]
            data = {}
            data['id'] = best_flight['id']
            data['price'] = best_flight['price']
            carriers = []
            actual_carriers = []
            for route in best_flight['routes']:
                for segment in route['segments']:
                    if segment['carrier'] not in carriers:
                        carriers.append(segment['carrier'])
                    if segment['actual_carrier'] not in actual_carriers:
                        actual_carriers.append(segment['actual_carrier'])
            data['carriers'] = carriers
            data['actual_carriers'] = actual_carriers
            #data['carriercode'] = best_flight['start_flights'][0]['start_routes'][0]['code']
            #data['start_duration'] = best_flight['start_flights'][0]['duration']
            #data['end_duration'] = best_flight['end_flights'][0]['duration']
            data['durations'] = [item['duration'] for item in best_flight['routes']]
            if mult == 0:
                data['start_date'] = kw['departure']
                data['end_date'] = kw['returning']
            elif mult == 1:
                data['departures'] = kw['departure']
            if cheapest_flights.get(data['price']) is None:
                cheapest_flights[data['price']] = []
            cheapest_flights[data['price']].append(data)
    prices = list(cheapest_flights.keys())
    prices.sort()
    return cheapest_flights[prices[0]]