import urllib2, datetime, re, time
from bs4 import BeautifulSoup

codechef_contest_link = "https://www.codechef.com/contests"
page = urllib2.urlopen(codechef_contest_link)
soup = BeautifulSoup(page, "html.parser")
list = soup.find_all("h3")
contest = soup.find_all("table", class_="dataTable")
if list[0].text == "Present Contests":
    contest = contest[0].find_all("tr")[1]
    contest = contest.find_all("td")
    contest_name = contest[1].text
    start = contest[3]["data-endtime"]
    t = time.strptime(start[0:19], '%Y-%m-%dT%H:%M:%S')
    if start[20] == '+':
        t -= datetime.timedelta(hours=int(start[21:24]), minutes=int(start[25:]))
    elif start[20] == '-':
        t += datetime.timedelta(hours=int(start[21:24]), minutes=int(start[25:]))
    now = time.mktime(t)
    then = int(time.time())
    d = divmod(now - then, 86400)
    h = divmod(d[1], 3600)
    m = divmod(h[1], 60)
    s = m[1]
    speech_output = "The contest " + contest_name + " on codechef is running. It will end in " \
                    '%d days, %d hours, %d minutes, %d seconds' % (d[0], h[0], m[0], s)
else:
    speech_output = "There is no contest running on codechef."

print speech_output

contest = soup.find_all("table", class_="dataTable")
if list[0].text == "Future Contests":
    contest = contest[0].find_all("tr")[1]
elif list[1].text == "Future Contests":
    contest = contest[1].find_all("tr")[1]
else:
    contest = None

if contest is not None:
    contest = contest.find_all("td")
    contest_name = contest[1].text
    start = contest[2]["data-starttime"]
    t = time.strptime(start[0:19], '%Y-%m-%dT%H:%M:%S')
    if start[20] == '+':
        t -= datetime.timedelta(hours=int(start[21:24]), minutes=int(start[25:]))
    elif start[20] == '-':
        t += datetime.timedelta(hours=int(start[21:24]), minutes=int(start[25:]))
    now = time.mktime(t)
    then = int(time.time())
    d = divmod(now - then, 86400)
    h = divmod(d[1], 3600)
    m = divmod(h[1], 60)
    s = m[1]
    speech_output = "The next contest " + contest_name + " on codechef will start in " \
                                                    '%d days, %d hours, %d minutes, %d seconds' % (d[0], h[0], m[0], s)
else:
    speech_output = "There are no upcoming contest on codechef."

print speech_output