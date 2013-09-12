"""Module for handling autocomplete's part of the API"""

from domain.constants import API_BASE
from domain.general import send_post, get, validate_params

BASE = API_BASE + "autocomplete/"

def search_generic(term, flow="", sort=""):
    """Call the generic autocomplete API.
    
    term: search term
    flow: either 'hotels' or 'flights'
    sort: indicates the order of the objects returned (e.g. 'airports,cities').
    """
    validate_params([term, flow, sort])
    return get(BASE + str(term) + "?flow=" + flow + "&sort=" + sort)

def search_cities(term):
    """Only search for cities"""
    validate_params([term])
    return get(BASE + "cities/" + str(term))

def search_airports(term):
    """Only search for airports"""
    validate_params([term])
    return get(BASE + "airports/" + str(term))

def search_airline(term):
    """Only search for airlines"""
    validate_params([term])
    return get(BASE + "airlines/" + str(term))