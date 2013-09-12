"""Module for handling flights' part of the API"""

from domain.constants import API_BASE
from domain.general import send_post, get

BASE = API_BASE + "availability/flights/"

def get_roundtrip_flight(orig, to, departure, returning, adults="1", 
                         children="0", infants="0", cabintype="ECONOMY", 
                         stops="MORE_THAN_ONE"):
    return get(BASE + "roundTrip" + "/" + orig + "/" + to + "/" + departure \
        + "/" + returning + "/" + adults + "/" + children + "/" + infants \
        + "?cabintype=" + cabintype + "&stopsadvancedparameter" + stops)