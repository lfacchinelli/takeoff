from domain.constants import API_BASE
from domain.general import send_post, get

BASE = API_BASE + "countries/"

def get_country(code):
	return get(BASE + str(code))