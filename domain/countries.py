"""Module for handling countries' part of the API"""

from domain.constants import API_BASE
from domain.general import send_post, get, validate_params

BASE = API_BASE + "countries/"

def get_country(code):
    validate_params([code])
    response = get(BASE + str(code))
    if 'countries' in response:
        return response['countries'][0]