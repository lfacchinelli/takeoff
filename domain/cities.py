import json
import urllib2

from domain.constants import API_BASE
from domain.general import send_post, get

BASE = API_BASE + "cities"

def get_city(code):
	return get(BASE + "/" + str(code))