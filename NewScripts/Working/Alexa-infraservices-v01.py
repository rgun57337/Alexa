"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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
####   Begin of Standard Functions   ####
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa infra smart services. " \
                    "Choose the services you would like to manage. " \
                    "The currently supported services are backup, monitoring, Operations. " \
                    "You may say. Open backup services. "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me how may I help you. " \
                    "Choose the services you would like to manage. " \
                    "The currently supported services are backup, monitoring, Operations. " \
                    "You may say. Open backup services. "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

####   End of Standard Functions   ####

def createAMIBackups(VPCid):
    ec2 = boto3.resource('ec2').Vpc(id=VPCid)
    instances = []
    result = ec2.instances.all()
    print(result)
    for instance in result:
        instances.append(instance.id)

    now = datetime.datetime.now()
    print(now)
    for inst in instances:
        ec2Details = boto3.client('ec2')
        AMIid = ec2Details.create_image(InstanceId=inst, Name="Lambda-"+inst+"-"+now.strftime("%Y-%m-%d-%H-%M"), Description="Alexa created AMI of instance "+inst, NoReboot=True, DryRun=False)
        print(AMIid)

def backupType_attributes(backup_type):
    return {"backupType": backup_type}

def backupIntent_function(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'value' in intent['slots']['backupSlot']:
        backup_type = intent['slots']['backupSlot']['value']
        session_attributes = backupType_attributes(backup_type)
        speech_output = "You choosed the backup option as " + \
                        backup_type.upper() + ". " \
                        "Tell me the envirment to backup. " \
                        "You may say take production backup. or. " \
                        "take development backup. "
        reprompt_text = "I'm not sure what is the backup type. " \
                        "You can say the backup type is AMI. "
    else:
        speech_output = "Choose the backup service type. " \
                        "The supported backup types are AMIs  and  snapshots. " \
                        "You may say AMI backups. "
        reprompt_text = "I'm not sure what is the backup type. " \
                        "You can say AMI backups. or . " \
                        "Snapshot backups. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def backupEnv_attributes(backup_env):
    return {"backupEnv": backup_env}

def backupEnvIntent_function(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'value' in intent['slots']['backupEnvSlot']:
        backup_env = intent['slots']['backupEnvSlot']['value']
        session_attributes = backupEnv_attributes(backup_env)

        if  backup_env == "production":
            should_end_session = True
            speech_output = "You choosed the backup option as " + \
                            backup_env + "environment. " \
                            "Taking backups. Thank you. "
            reprompt_text = "I'm not sure what is the backup enviromnet. " \
                            "You can say Take production backup. "
            createAMIBackups('vpc-82f089fa')
        elif backup_env == "development":
            should_end_session = True
            speech_output = "You choosed the backup option as " + \
                            backup_env + "environment. " \
                            "Taking backups. Thank you. "
            reprompt_text = "I'm not sure what is the backup enviromnet. " \
                            "You can say take production backup. "
            createAMIBackups('vpc-65f28b1d')
        elif backup_env == "stage":
            should_end_session = True
            speech_output = "You choosed the backup option as " + \
                            backup_env + "environment. " \
                            "Taking backups. Thank you. "
            reprompt_text = "I'm not sure what is the backup enviromnet. " \
                            "You can say take production backup. "
            createAMIBackups('vpc-73ff860b')
        else:
            speech_output = "I'm not sure what is the backup enviromnet. " \
                            "You can say take production backup. or. " \
                            "Take development backup."
            reprompt_text = "I'm not sure what is the backup enviromnet. " \
                            "You can say take production backup. or. " \
                            "Take development backup. "
    else:
        speech_output = "Choose the backup service environment. " \
                        "The supported backup types are production, stage  and  development." \
                        "You may say take production backup. "
        reprompt_text = "I'm not sure what is the backup environment. " \
                        "You can say take production backup. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def aws_cloudwatch_func():
    alarmStates = ['OK','ALARM','INSUFFICIENT_DATA']
    alarmResponse = ""
    client = boto3.client('cloudwatch', region_name='us-east-1')
    for alarmState in alarmStates:
        message = client.describe_alarms(
            StateValue=alarmState,
            MaxRecords=100
        )
        alarmResponse += str("There are " + str(len(message[u'MetricAlarms'])) + " servers in cloud watch " + str(alarmState) + " state    ."+'\n')
    return alarmResponse;

def protalStatus(urls):
    import httplib
    from urlparse import urlparse

    def checkUrl(url):
        p = urlparse(url)
        conn = httplib.HTTPConnection(p.netloc)
        conn.request('HEAD', p.path)
        resp = conn.getresponse()
        return resp.status

    workingURLS = []
    nonWorkingURLs = []
    responseURLs = ""
    for url in urls:
        if checkUrl(url) == 200:
            workingURLS.append(url)
        else:
            nonWorkingURLs.append(url)

    if len(nonWorkingURLs) > 0:
        responseURLs += str(len(nonWorkingURLs)) + " URLs are down . They are . \n"
        for nonWorkingURL in nonWorkingURLs:
            responseURLs += nonWorkingURL + " . \n"
    else:
        responseURLs = "All the URLs up and running."

    return responseURLs

def monitorType_attributes(monitor_type):
    return {"monitorType": monitor_type}

def monitorIntent_function(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'value' in intent['slots']['monitorSlot']:
        monitor_type = intent['slots']['monitorSlot']['value']
        session_attributes = monitorType_attributes(monitor_type)
        speech_output = "You choosed the monitor option as " + \
                        monitor_type.upper() + ". " \
                        "Tell me the envirment to monitor. " \
                        "You may say get cloudwatch reports. or. " \
                        "get nagios reports. "
        reprompt_text = "I'm not sure what is the monitoring type. " \
                        "You may say get cloudwatch report. or. " \
                        "get nagios report. "
    else:
        speech_output = "Choose the monitoring type. " \
                        "The supported monitoring services are cloudwatch, nagios and healthcheck. " \
                        "You may say get cloudwatch report. or. " \
                        "get nagios report. " \
                        "get development healthcheck report. "
        reprompt_text = "I'm not sure what is the monitoring type. " \
                        "You can say get cloudwatch report. or . " \
                        "get nagios report. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def monitorEnv_attributes(backup_env):
    return {"backupEnv": backup_env}

def monitorEnvIntent_function(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'value' in intent['slots']['monitorEnvSlot']:
        monitor_env = intent['slots']['monitorEnvSlot']['value']
        session_attributes = monitorEnv_attributes(monitor_env)

        if  monitor_env == "cloudwatch":
            should_end_session = True
            speech_output = "Fetching the " + \
                            monitor_env + " report. " \
                            "Please wait. Thank you. " + \
                            aws_cloudwatch_func()
            reprompt_text = "I'm not sure what is the monitor type. " \
                            "You can say get cloudwatch report. "
        elif monitor_env == "nagios":
            should_end_session = True
            speech_output = "Fetching the " + \
                            monitor_env + " report. " \
                            "Currently the service is in development stage. Please try later. Thank you. "
            reprompt_text = "I'm not sure what is the backup enviromnet. " \
                            "You can say get cloudwatch report. "
        elif monitor_env == "development healthcheck":
            should_end_session = True
            speech_output = "Fetching the " + \
                            monitor_env + " report. Please wait. " + \
                            protalStatus(devMonitorURLs)
            reprompt_text = "I'm not sure what is the backup enviromnet. " \
                            "You can say get cloudwatch report. "
        else:
            speech_output = "I'm not sure what is the monitoring type. " \
                            "You may say get cloudwatch report. or. " \
                            "get nagios report. " \
                            "get development healthcheck report. "
            reprompt_text = "I'm not sure what is the monitoring type. " \
                            "You may say get cloudwatch report. or. " \
                            "get nagios report. " \
                            "get development healthcheck report. "
    else:
        speech_output = "Choose the monitoring type. " \
                        "The supported monitoring types are cloudwatch and nagios. " \
                        "You may say get cloudwatch report. or. " \
                        "get nagios report. " \
                        "get development healthcheck report. "
        reprompt_text = "I'm not sure what is the monitoring type. " \
                        "You may say get cloudwatch report. or. " \
                        "get nagios report. " \
                        "get development healthcheck report. "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def operationIntent_function(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_snow_incident(SNOWurl, SNOWuser, SNOWpwd):
    #Need to install requests package for python
    #easy_install requests
    import requests
    import json

    # Set the request parameters
    #SNOWurl = 'https://dev33601.service-now.com/api/now/v1/table/incident123'

    # Eg. User name="admin", Password="admin" for this code sample.
    #SNOWuser = 'admin'
    #SNOWpwd = 'Password@123'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    data = {"short_description" : "This is the short description", "description":"This is the description"}
    data_json = json.dumps(data)
    # Do the HTTP request
    #response = requests.get(url, auth=(user, pwd), headers=headers  )
    response = requests.post(SNOWurl, data=data_json, auth=(SNOWuser, SNOWpwd), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 201:
        #print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        #exit()
        snowResponse = "Faild to create an incident. Please contact administrator"
    else:
        snowResponse = "Created an incident. " + response.json()['result']['number'] + " "
    # Decode the JSON response into a dictionary and use the data
    #data = response
    #print(data)
    return snowResponse

def incident_attributes(incident_ops):
    return {"incidentOps": incident_ops}

def incidentIntent_function(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'value' in intent['slots']['incidentSlot']:
        incident_ops = intent['slots']['incidentSlot']['value']
        session_attributes = incident_attributes(incident_ops)

        if  incident_ops == "open incident":
            should_end_session = True
            speech_output = "Creating incident in service now. " \
                            "Please wait. Thank you. " + \
                            create_snow_incident(SNOWurl, SNOWuser, SNOWpwd)
            reprompt_text = "I'm not sure what is the service now incident operation. " \
                            "You can say create incident in service now. "
        elif incident_ops == "resolve incident":
            should_end_session = True
            speech_output = "resolve incident is currently in development. Please try later. Thank you. "
            reprompt_text = "I'm not sure what is the service now incident operation. " \
                            "You can say create incident in service now. "
        elif incident_ops == "get incident":
            should_end_session = True
            speech_output = "Fetching the " + \
                            monitor_env + " report. Please wait. "
            reprompt_text = "I'm not sure what is the service now incident operation. " \
                            "You can say create incident in service now. "
        else:
            speech_output = "I'm not sure what is the service now incident operation. " \
                            "You can say create incident in service now. " \
                            "resolve incident in service now. " \
                            "get incident in service now. "
            reprompt_text = "I'm not sure what is the service now incident operation. " \
                            "You can say create incident in service now. "
    else:
        speech_output = "Choose the incident operation type. " \
                        "The supported incident operations are create incident, resolve incident and get incident. " \
                        "You may say open incident in service now. or. " \
                        "resolve incident in service now. " \
                        "get incident in service now. "
        reprompt_text = "I'm not sure what is the service now incident operation. " \
                        "You can say create incident in service now. "
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
    if intent_name == "backupIntent":
        return backupIntent_function(intent, session)
    elif intent_name == "backupEnvIntent":
            return backupEnvIntent_function(intent, session)
    elif intent_name == "monitorIntent":
        return monitorIntent_function(intent, session)
    elif intent_name == "monitorEnvIntent":
        return monitorEnvIntent_function(intent, session)
    elif intent_name == "operationIntent":
        return operationIntent_function(intent, session)
    elif intent_name == "emailIntent":
        return emailIntent_function(intent, session)
    elif intent_name == "incidentIntent":
        return incidentIntent_function(intent, session)
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

# --------------- Variables ---------------------
devMonitorURLs = ['http://www.stackoverflow.com','https://www.google.com','http://youtube.com']
SNOWurl = 'https://dev33601.service-now.com/api/now/v1/table/incident123'
SNOWuser = 'admin'
SNOWpwd = 'Password@123'
# --------------- Main handler ------------------
import boto3
import json
import datetime

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