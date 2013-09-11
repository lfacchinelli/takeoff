import urllib2
import json

def send_post(content, url):
	payload = json.loads(content)
	req = urllib2.Request(url, payload, {'Content-Type': 'application/json'})
	req2 = urllib2.urlopen(req)
	response = req2.read()
	req2.close()
	return response

def get(url):
	req = urllib2.urlopen(url)
	import pdb
	pdb.set_trace()
	payload = json.loads(req.read())
	return payload

""" Somewhere around here we must use this

>>> import gzip
>>> from StringIO import StringIO
>>> buf = StringIO(content)
>>> f = gzip.GzipFile(fileobj=buf)
>>> data = f.read()
>>> data
'{"cities":[{"internalId":"1","countryId":"PF","id":"AAA","name":"Anaa","geoLocation":{"longitude":-145.51,"latitude":-17.3526}}],"meta":{"time":"3ms","reference":"api-02-61949-oB6JeigwqY"}}'
>>>

Stupid stupid STUPID despegar.com sends API data gzipped, even though we haven't asked for it.

"""