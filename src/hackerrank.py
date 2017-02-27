import urllib2, datetime, re, time
from bs4 import BeautifulSoup

hackerrank_contest_link = "https://www.hackerrank.com/contests"
page = urllib2.urlopen(hackerrank_contest_link)
soup = BeautifulSoup(page, "html.parser")
list = soup.find_all("div", class_="active_contests")
speech_output = "There are no upcoming contest on hackerrank."
if len(list) > 0:
    list = list[0].find_all('li')
    list.pop(0)
    if len(list) > 0:
        contest = []
        for r in list:
            temp = r.find_all('button')
            if len(temp) > 0 and temp[0].text == "Sign Up":
                contest = r
                contest_name = contest.find_all('span')[0].text
                start = contest.find_all('meta')[0]["content"]
                start = time.strptime(start[0:19], '%Y-%m-%dT%H:%M:%S')
                start = time.mktime(start)
                end = contest.find_all('meta')[1]["content"]
                end = time.strptime(end[0:19], '%Y-%m-%dT%H:%M:%S')
                end = time.mktime(end)
                then = int(time.time())
                if then < start:
                    now = start
                else:
                    now = end
                d = divmod(now - then, 86400)
                h = divmod(d[1], 3600)
                m = divmod(h[1], 60)
                s = m[1]
                if then < start:
                    speech_output = "The next contest " + contest_name + " on hackerrank will start in next " \
                            '%d days, %d hours, %d minutes, %d seconds' % (d[0], h[0], m[0], s)
                    break
        '''else:
            speech_output = "The contest " + contest_name + " on Hackerrank is running and it will end in " \
                                                            '%d days, %d hours, %d minutes, %d seconds' % (
                                                            d[0], h[0], m[0], s)'''

print speech_output

hackerrank_contest_link = "https://www.hackerrank.com/contests"
page = urllib2.urlopen(hackerrank_contest_link)
soup = BeautifulSoup(page, "html.parser")
list = soup.find_all("div", class_="active_contests")
speech_output = "There is no contest running on hackerrank."

if len(list) > 0:
    list = list[0].find_all('li')
    list.pop(0)
    if len(list) > 0:
        contest = []
        for r in list:
            temp = r.find_all('button')
            if len(temp) > 0 and temp[0].text == "Sign Up":
                contest = r
                break
        contest_name = contest.find_all('span')[0].text
        start = contest.find_all('meta')[0]["content"]
        start = time.strptime(start[0:19], '%Y-%m-%dT%H:%M:%S')
        start = time.mktime(start)
        end = contest.find_all('meta')[1]["content"]
        end = time.strptime(end[0:19], '%Y-%m-%dT%H:%M:%S')
        end = time.mktime(end)
        then = int(time.time())
        if then < start:
            now = start
        else:
            now = end
        d = divmod(now - then, 86400)
        h = divmod(d[1], 3600)
        m = divmod(h[1], 60)
        s = m[1]

        if then > start:
            speech_output = "The contest " + contest_name + " on hackerrank is running and it will end in " \
                            '%d days, %d hours, %d minutes, %d seconds' % (d[0], h[0], m[0], s)

print speech_output