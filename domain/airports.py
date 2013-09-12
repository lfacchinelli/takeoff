"""Module for handling airports' part of the API"""

from domain.constants import API_BASE
from domain.general import send_post, get, validate_params

BASE = API_BASE + "airports/"

def get_airport(code):
    """Get an airport based on a 3-letter code"""
    validate_params([code])
    response = get(BASE + str(code))
    if 'airports' in response:
        return response['airports'][0]