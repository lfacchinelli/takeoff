#!/usr/bin/env python3

from domain.constants import API_BASE
from domain.general import *


class currencies(object):
    '''Module for handling currencies' part of the API'''

    def __init__(self):
        '''Init Method'''
        self.BASE = API_BASE + "currencies/"