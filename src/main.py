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
                    "When is the codeforces next contest."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me from where you want the contest details by saying, " \
                    "When is the codeforces next contest."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Amazon Alexa Contest Notify Skills Kit. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def getNextCodechefContest(intent, session):
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
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def getCurrrentCodechefContest(intent, session):
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
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def getNextHackerrankContest(intent, session):
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
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def getCurrrentHackerrankContest(intent, session):
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
    website = intent_request['intent']['slots']['WebsiteName']['value']

    # Dispatch to your skill's intent handlers
    if intent_name == "NextContestIntent" and website.lower() == "codechef":
        return getNextCodechefContest(intent, session)
    elif intent_name == "CurrentContestIntent" and website.lower() == "codechef":
        return getCurrrentCodechefContest(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
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
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
