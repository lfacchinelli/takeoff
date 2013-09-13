#!/usr/bin/env python3

from domain.constants import API_BASE
from domain.general import *


class cities(object):
    '''Module for handling cities' part of the API'''

    def __init__(self):
        '''Init Method'''
        self.BASE = API_BASE + "cities/"

    def get_city(self, code):
        '''Get the city from the code'''
        validate_params([code])
        response = get(self.BASE + str(code))
        if 'cities' in response:
            return response['cities'][0]