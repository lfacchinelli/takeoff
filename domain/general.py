import urllib.request, urllib.error, urllib.parse
import json
import gzip
from io import StringIO

def send_post(content, url):
    payload = json.loads(content)
    req = urllib.request.Request(url, payload, 
                                 {'Content-Type': 'application/json'})
    req2 = urllib.request.urlopen(req)
    response = req2.read()
    req2.close()
    return response

def get(url):
    """Get the json object at url
    
    despegar.com sends API data gzipped, even though we haven't asked for it.
    As such, we must use gzip to decompress it first.
    """
    req = urllib.request.urlopen(url)
    buffer = StringIO(req.read())
    f_ = gzip.GzipFile(fileobj=buffer)
    content = f_.read()
    f_.close()
    payload = json.loads(content)
    return payload

def validate_params(paramlist):
    """Ensure parameters passed are valid strings"""
    for param in paramlist:
        if not isinstance(param, str) or ' ' in param:
            raise TypeError("Parameters must ALWAYS be strings without spaces.")