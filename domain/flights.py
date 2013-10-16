"""Module for handling flights' part of the API"""

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
                  "&stopsadvancedparameter" + stops)
    result = {}
    if 'flights' in content:
        result['flights'] = content['flights']
    if 'meta' in content:
        if 'summaryMatrix' in content['meta']:
            result['matrix'] = content['meta']['summaryMatrix']
    
    # Based on both parts of result, specific info can be obtained, like:
    #>>> for item in res['flights']:
    #...  if item['id'] == 'C_141258592_457465048_-1265597135_-430519781':
    #...   pprint.pprint(item)

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
                ids.append(id)
    best_flights = []
    for id in ids:
        best_flights.append([flight for flight in flights_raw['flights'] if flight['id'] == id][0])
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
        out_flights = []
        for item in flight['outboundRoutes']:
            out_flight = {}
            out_flight['duration'] = item['duration']
            out_flight['changes_airport'] = item['hasAirportChange']
            out_flight['start_routes'] = []
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
                out_flight['start_routes'].append(segment)
            out_flights.append(out_flight)
        summary_flight['start_flights'] = out_flights
        in_flights = []
        for item in flight['inboundRoutes']:
            in_flight = {}
            in_flight['duration'] = item['duration']
            in_flight['changes_airport'] = item['hasAirportChange']
            in_flight['end_routes'] = []
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
                in_flight['end_routes'].append(segment)
            in_flights.append(in_flight)
        summary_flight['end_flights'] = in_flights
        summary.append(summary_flight)
    return summary