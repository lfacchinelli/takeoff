#!/usr/bin/env python3

from domain.constants import API_BASE
from domain.general import *


class fligths(object):
    '''Module for handling flights' part of the API'''
    def __init__(self):
        '''Init Method'''
        self.BASE = API_BASE + "availability/flights/"

    def get_roundtrip_flight(self, orig, to, departure, returning, adults="1",
                             children="0", infants="0", cabintype="ECONOMY",
                             stops="MORE_THAN_ONE"):
        return get(self.BASE + "roundTrip" + "/" + orig + "/" + to + "/"
            + departure + "/" + returning + "/" + adults + "/" + children
            + "/" + infants + "?cabintype=" + cabintype
            + "&stopsadvancedparameter" + stops)