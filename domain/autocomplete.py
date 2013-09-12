from domain.constants import API_BASE
from domain.general import send_post, get

BASE = API_BASE + "autocomplete/"

def auto_generic(term, flow="", sort=""):
	"""Call the generic autocomplete API.
	
	term: search term
	flow: either 'hotels' or 'flights'
	sort: indicates the order of the objects returned (e.g. 'airports,cities').
	"""
	
	return get(BASE + str(term) + "?flow=" + flow + "&sort=" + sort)

def auto_cities(term):
	"""Only search for cities"""
	return get(BASE + "cities/" + term)

def auto_airports(term):
	"""Only search for airports"""
	return get(BASE + "airports/" + term)

def auto_airline(term):
	"""Only search for airlines"""
	return get(BASE + "airlines/" + term)