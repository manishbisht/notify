import urllib, json, time
url = "http://codeforces.com/api/contest.list?gym=false"
response = urllib.urlopen(url)
data = json.loads(response.read())
if data["status"] == "OK":
	result = [];
	for d in data["result"]:
		if d["phase"] != "BEFORE":
			break
		result = d
	if result == []:
		print "No data";
	else:
		print result["name"]
	now = result["startTimeSeconds"] # epoch seconds
	then = int(time.time()) # some time in the past

	d = divmod(now-then,86400)  # days
	h = divmod(d[1],3600)  # hours
	m = divmod(h[1],60)  # minutes
	s = m[1]  # seconds

	print '%d days, %d hours, %d minutes, %d seconds' % (d[0],h[0],m[0],s)
else:
	print "sasas"
