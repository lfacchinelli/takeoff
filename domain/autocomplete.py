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
    response = get(BASE + str(term) + "?flow=" + flow + "&sort=" + sort)
    if 'autocomplete' in response:
        return response['autocomplete']

def search_cities(term):
    """Only search for cities"""
    response = get(BASE + "cities/" + str(term))
    if 'autocomplete' in response:
        return response['autocomplete']

def search_airports(term):
    """Only search for airports"""
    response = get(BASE + "airports/" + str(term))
    if 'autocomplete' in response:
        return response['autocomplete']

def search_airlines(term):
    """Only search for airlines"""
    response = get(BASE + "airlines/" + str(term))
    if 'data' in response:
        return response['data']