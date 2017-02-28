import urllib, json, time

url = "http://codeforces.com/api/contest.list?gym=false"
response = urllib.urlopen(url)
data = json.loads(response.read())
speech_output = "There are no upcoming contest on codeforces."
if data["status"] == "OK":
    result = []
    for d in data["result"]:
        if d["phase"] == "FINISHED":
            break
        result = d
    if result == []:
        speech_output = "There are no upcoming contest on codeforces."
    else:
        now = result["startTimeSeconds"]
        then = int(time.time())
        d = divmod(now - then, 86400)
        h = divmod(d[1], 3600)
        m = divmod(h[1], 60)
        s = m[1]
        speech_output = "The next contest on codeforces " + result["name"] + " will start in " \
                                                                             '%d days, %d hours, %d minutes, %d seconds' % (
                                                                                 d[0], h[0], m[0], s)
print speech_output

url = "http://codeforces.com/api/contest.list?gym=false"
response = urllib.urlopen(url)
data = json.loads(response.read())
speech_output = "There is no contest running on codeforces."
if data["status"] == "OK":
    result = []
    for d in data["result"]:
        result = d
        if d["phase"] == "CODING":
            break
        elif d["phase"] == "FINISHED":
            result = []
            break
    if result == []:
        speech_output = "There is no contest running on codeforces."
    else:
        now = result["startTimeSeconds"] + result["durationSeconds"]
        then = int(time.time())
        d = divmod(then - now, 86400)
        h = divmod(d[1], 3600)
        m = divmod(h[1], 60)
        s = m[1]
        speech_output = "The contest " + result["name"] + " will end in " \
                                                          '%d days, %d hours, %d minutes, %d seconds' % (
                                                              d[0], h[0], m[0], s)
print speech_output
