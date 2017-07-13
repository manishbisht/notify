"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6
For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urllib, json, time, urllib2, datetime
import bs4


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Amazon Alexa Contest Notify Skills Kit. " \
                    "Please tell me from where you want the contest details by saying, " \
                    "When is the codeforces next contest or Is there any contest running on codechef."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me from where you want the contest details by saying, " \
                    "When is the codeforces next contest."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def getHelpContent():
    session_attributes = {}
    card_title = "Help Content"
    speech_output = "I am here to update you about the current and future programming contest " \
                    "available on different websites like codeforces, codechef and hackerrank. " \
                    "You can ask me questions like When is the codefoces next contest, " \
                    "when is the next hackerrank contest or Is there any contest running on codechef. " \
                    "Right now I support only codeforces, codechef and hackerrank."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me from where you want the contest details by saying, " \
                    "When is the codeforces next contest."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def getErrorMessage():
    session_attributes = {}
    card_title = "Help Content"
    speech_output = "If you just said something then I can't understand it. " \
                    "Please ask me questions by saying When is the codefoces next contest, " \
                    "or Is there any contest running on codechef. " \
        # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me from where you want the contest details by saying, " \
                    "When is the codeforces next contest."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def googleActionsError():
    speech_output = "If you just said something then I can't understand it. " \
                    "Please try again later."
    return {"speech": speech_output}

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Amazon Alexa Contest Notify Skills Kit. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def nextContest(intent, session):
    """ Get the next contest details and prepares the speech to reply to the user.
    """
    if 'WebsiteName' in intent['slots']:
        website = intent['slots']['WebsiteName']
        if 'value' in website:
            website = website['value']
            if website.lower() == "codeforces" or website.lower() == "code forces":
                return getNextCodeforcesContest()
            elif website.lower() == "codechef" or website.lower() == "code chef":
                return getNextCodechefContest()
            elif website.lower() == "hackerrank" or website.lower() == "hacker rank":
                return getNextHackerrankContest()
            else:
                return getErrorMessage()
        else:
            return getErrorMessage()
    else:
        return getErrorMessage()

def currentContest(intent, session):
    """ Get the current contest details and prepares the speech to reply to the user.
    """
    if 'WebsiteName' in intent['slots']:
        website = intent['slots']['WebsiteName']
        if 'value' in website:
            website = website['value']
            if website.lower() == "codeforces" or website.lower() == "code forces":
                return getCurrrentCodeforcesContest()
            elif website.lower() == "code chef" or website.lower() == "code chef":
                return getCurrrentCodechefContest()
            elif website.lower() == "hackerrank" or website.lower() == "hacker rank":
                return getCurrrentHackerrankContest()
            else:
                return getErrorMessage()
        else:
            return getErrorMessage()
    else:
        return getErrorMessage()

def getNextCodeforcesContest(type=None):
    """ Get the next codeforces contest details and prepares the speech to reply to the user.
    """
    card_title = "Codeforces Next Contest Details"
    session_attributes = {}
    should_end_session = True
    reprompt_text = ""
    url = "http://codeforces.com/api/contest.list?gym=false"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    speech_output = "There are no upcoming contest on codeforces."
    if data["status"] == "OK":
        result = []
        for d in data["result"]:
            if d["phase"] != "BEFORE":
                break
            result = d
        if not result:
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
    if type:
        return {"speech": speech_output}
    else:
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))


def getCurrrentCodeforcesContest(type=None):
    """ Get the current codeforces contest details and prepares the speech to reply to the user.
    """
    card_title = "Codeforces Current Contest Details"
    session_attributes = {}
    should_end_session = True
    reprompt_text = ""
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
            then = result["startTimeSeconds"] + result["durationSeconds"]
            now = int(time.time())
            d = divmod(then - now, 86400)
            h = divmod(d[1], 3600)
            m = divmod(h[1], 60)
            s = m[1]
            speech_output = "The contest " + result["name"] + " will end in " \
                                                              '%d days, %d hours, %d minutes, %d seconds' % (
                                                                  d[0], h[0], m[0], s)
    if type:
        return {"speech": speech_output}
    else:
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))


def getNextCodechefContest(type=None):
    """ Get the next codechef contest details and prepares the speech to reply to the user.
    """
    card_title = "Codechef Next Contest Details"
    session_attributes = {}
    should_end_session = True
    reprompt_text = ""
    codechef_contest_link = "https://www.codechef.com/contests"
    page = urllib2.urlopen(codechef_contest_link)
    soup = bs4.BeautifulSoup(page, "html.parser")
    list = soup.find_all("h3")
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
                                                             '%d days, %d hours, %d minutes, %d seconds' % (
                                                                 d[0], h[0], m[0], s)
    else:
        speech_output = "There are no upcoming contest on codechef."
    if type:
        return {"speech": speech_output}
    else:
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))


def getCurrrentCodechefContest(type=None):
    """ Get the current codechef contest details and prepares the speech to reply to the user.
    """
    card_title = "Codechef Current Contest Details"
    session_attributes = {}
    should_end_session = True
    reprompt_text = ""
    codechef_contest_link = "https://www.codechef.com/contests"
    page = urllib2.urlopen(codechef_contest_link)
    soup = bs4.BeautifulSoup(page, "html.parser")
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
                                                        '%d days, %d hours, %d minutes, %d seconds' % (
                                                            d[0], h[0], m[0], s)
    else:
        speech_output = "There is no contest running on codechef."
    if type:
        return {"speech": speech_output}
    else:
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))


def getNextHackerrankContest(type=None):
    """ Get the next hackerrank contest details and prepares the speech to reply to the user.
    """
    card_title = "Hackerrank Next Contest Details"
    session_attributes = {}
    should_end_session = True
    reprompt_text = ""
    hackerrank_contest_link = "https://www.hackerrank.com/contests"
    page = urllib2.urlopen(hackerrank_contest_link)
    soup = bs4.BeautifulSoup(page, "html.parser")
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
                                                                             '%d days, %d hours, %d minutes, %d seconds' % (
                                                                                 d[0], h[0], m[0], s)
                        break
    if type:
        return {"speech": speech_output}
    else:
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))


def getCurrrentHackerrankContest(type=None):
    """ Get the current hackerrank contest details and prepares the speech to reply to the user.
    """
    card_title = "Hackerrank Current Contest Details"
    session_attributes = {}
    should_end_session = True
    reprompt_text = ""
    hackerrank_contest_link = "https://www.hackerrank.com/contests"
    page = urllib2.urlopen(hackerrank_contest_link)
    soup = bs4.BeautifulSoup(page, "html.parser")
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
                                                                '%d days, %d hours, %d minutes, %d seconds' % (
                                                                    d[0], h[0], m[0], s)
    if type:
        return {"speech": speech_output}
    else:
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "NextContestIntent":
        return nextContest(intent, session)
    elif intent_name == "CurrentContestIntent":
        return currentContest(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return getHelpContent()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    if 'id' in event:
        if event['result']['metadata']['intentName'] == 'NextContestIntent':
            if event['result']['parameters']['WebsiteName'] == "codeforces":
                return getNextCodeforcesContest(event['result']['source'])
            elif event['result']['parameters']['WebsiteName'] == "codechef":
                return getNextCodechefContest(event['result']['source'])
            elif event['result']['parameters']['WebsiteName'] == "hackerrank":
                return getNextHackerrankContest(event['result']['source'])
            else:
                return googleActionsError()
        elif event['result']['metadata']['intentName'] == 'CurrentContestIntent':
            if event['result']['parameters']['WebsiteName'] == "codeforces":
                return getCurrrentCodeforcesContest(event['result']['source'])
            elif event['result']['parameters']['WebsiteName'] == "codechef":
                return getCurrrentCodechefContest(event['result']['source'])
            elif event['result']['parameters']['WebsiteName'] == "hackerrank":
                return getCurrrentHackerrankContest(event['result']['source'])
            else:
                return googleActionsError()
        else:
            return googleActionsError()

    else:
        print("event.session.application.applicationId=" +
            event['session']['application']['applicationId'])

        if event['session']['new']:
            on_session_started({'requestId': event['request']['requestId']}, event['session'])

        if event['request']['type'] == "LaunchRequest":
            return on_launch(event['request'], event['session'])
        elif event['request']['type'] == "IntentRequest":
            return on_intent(event['request'], event['session'])
        elif event['request']['type'] == "SessionEndedRequest":
            return on_session_ended(event['request'], event['session'])