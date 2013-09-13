#!/usr/bin/env python3

from domain.constants import API_BASE
from domain.general import *


class autocomplete(object):
    '''Module for handling autocomplete's part of the API'''

    def __init__(self):
        '''Init Method'''
        self.BASE = API_BASE + "autocomplete/"

    def search_generic(self, term, flow="", sort=""):
        """Call the generic autocomplete API.
        term: search term
        flow: either 'hotels' or 'flights'
        sort: indicates the order of
        the objects returned (e.g. 'airports,cities').
        """
        validate_params([term, flow, sort])
        return get(self.BASE + str(term) + "?flow=" + flow + "&sort=" + sort)

    def search_cities(self, term):
        """Only search for cities"""
        validate_params([term])
        return get(self.BASE + "cities/" + str(term))

    def search_airports(self, term):
        """Only search for airports"""
        validate_params([term])
        return get(self.BASE + "airports/" + str(term))

    def search_airline(self, term):
        """Only search for airlines"""
        validate_params([term])
        return get(self.BASE + "airlines/" + str(term))