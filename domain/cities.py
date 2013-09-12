"""Module for handling cities' part of the API"""

from domain.constants import API_BASE
from domain.general import send_post, get, validate_params

BASE = API_BASE + "cities/"

def get_city(code):
    validate_params([code])
    response = get(BASE + str(code))
    if 'cities' in response:
        return response['cities'][0]