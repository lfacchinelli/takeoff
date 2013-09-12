from domain.constants import API_BASE
from domain.general import send_post, get

BASE = API_BASE + "airports/"

def get_airport(code):
	return get(BASE + str(code))