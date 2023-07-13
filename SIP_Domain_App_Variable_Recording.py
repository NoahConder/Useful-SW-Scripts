import os
from dotenv import load_dotenv
from flask import Flask, request
from pyngrok import ngrok
from signalwire.rest import Client as signalwire_client
from signalwire.voice_response import VoiceResponse, Dial

# Load our credentials
load_dotenv()
# TODO: Add your credentials to a .env before starting this up!)
# SIGNALWIRE Specific credentials.
projectID = os.getenv('SIGNALWIRE_PROJECT')
authToken = os.getenv('SIGNALWIRE_TOKEN')
spaceURL = os.getenv('SIGNALWIRE_SPACE')

client = signalwire_client(f"{projectID}", f"{authToken}", signalwire_space_url = f'{spaceURL}')

app = Flask(__name__)


@app.route('/dialer', methods=['POST'])
def dialer():
    response = VoiceResponse()
    from_number = request.form.get('SipUser')
    testing_sip_variable = request.form.get('SipHeader_X-FROM_NUM')
    testing_sip_variable_2 = request.form.get('SipHeader_X-FROM_TEST')
    testing_sip_variable_3 = request.form.get('SipHeader_X-FROM_HELLO_WORLD')

    print(from_number)
    print(testing_sip_variable)
    print(testing_sip_variable_2)
    print(testing_sip_variable_3)

    # TODO Be sure to swap the caller ID to one of your own! (Verified or SignalWire number)
    dial = Dial(caller_id='+1234567891', record='record-from-ringing')
    dial.number(f'{from_number}')
    response.append(dial)
    return response.to_xml()

def start_ngrok():
    # Set up a tunnel on port 5000 for our Flask object to interact locally
    url = ngrok.connect(5000).public_url
    print(' * Tunnel URL:', url + "/dialer")


if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        start_ngrok()

app.run(debug=True)

