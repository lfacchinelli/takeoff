#!/usr/bin/env python3

from domain.constants import API_BASE
from domain.general import *


class countries(object):
    '''Module for handling countries' part of the API'''

    def __init__(self):
        '''Init Method'''
        self.BASE = API_BASE + "countries/"

    def get_country(self, code):
        '''Get the country by the code'''
        validate_params([code])
        response = get(self.BASE + str(code))
        if 'countries' in response:
            return response['countries'][0]