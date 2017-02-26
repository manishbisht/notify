import requests
r = requests.post("http://api.topcoder.com/v2/auth", data={'username': 'manishbisht', 'password': 'Manish@2512510'})
if 'token' in r.json():
	print r.json()['token']
	rr = requests.post("http://api.topcoder.com/v2/data/srm/contests", data={'Authorization': 'Bearer '+r.json()['token']})
	print rr.json()
else:
	print None

from urllib2 import Request, urlopen

request = Request('http://api.topcoder.com/v2/data/srm/contests')

response_body = urlopen(request).read()
print response_body
