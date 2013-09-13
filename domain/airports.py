#!/usr/bin/env python3

from domain.constants import API_BASE
from domain.general import *


class airports(object):
    """Module for handling airports' part of the API"""

    def __init__(self):
        '''Init Method'''
        self.BASE = API_BASE + "airports/"

    def get_airport(self, code):
        '''Get an airport based on a 3-letter code'''
        validate_params([code])
        response = get(self.BASE + str(code))
        if 'airports' in response:
            return response['airports'][0]