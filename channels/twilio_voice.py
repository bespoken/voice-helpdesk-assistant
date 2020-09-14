from twilio.rest import Client

# -*- coding: utf-8 -*-
import json
import logging
from pydash import py_
from sanic import Blueprint, response
from twilio.rest import Client

from rasa.core.channels import InputChannel
from rasa.core.channels import UserMessage, OutputChannel
from rasa.core.channels.channel import CollectingOutputChannel

logger = logging.getLogger(__name__)

class TwilioInput(InputChannel):
    """Twilio input channel"""

    @classmethod
    def name(cls):
        return "twilio_voice"

    @classmethod
    def from_credentials(cls, credentials):
        if not credentials:
            cls.raise_missing_credentials_exception()

        return cls(credentials.get("account_sid"),
                   credentials.get("auth_token"),
                   credentials.get("twilio_number"))

    def __init__(self, account_sid, auth_token, twilio_number,
                 debug_mode=True):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_number = twilio_number
        self.debug_mode = debug_mode

    def blueprint(self, on_new_message):
        twilio_webhook = Blueprint('twilio_webhook', __name__)

        @twilio_webhook.route("/", methods=['GET'])
        async def health(request):
            return response.json({"status": "ok"})

        @twilio_webhook.route("/webhook", methods=['POST'])
        async def message(request):
            print(request.form) # The payload is form-encoded body
            sender = request.form.get('From', None)
            # text = request.values.get('Body', None)
            out = CollectingOutputChannel()
            await on_new_message(UserMessage("Hi", out, sender, input_channel='twilio_voice'))

            return self.prompt(out.messages[0]["text"])
        
        @twilio_webhook.route("/action", methods=['POST'])
        async def action(request):
            print("/action called - form: " + str(request.form))
            result = request.form.get('SpeechResult')
            sender = request.form.get('From', None)
            
            if (result):
                print("Result: " + result)
                out = CollectingOutputChannel()
                    
                # send the user message to Rasa & wait for the
                # response to be sent back
                await on_new_message(UserMessage(result, out, sender, input_channel='twilio_voice'))

                # extract the text from Rasa's response
                last_response = py_.nth(out.messages, -1)
                print('last message: ' + last_response["text"])
                return self.prompt(last_response["text"])
            else:
                return response.text("<Response>" \
                        "<Say>Please reply</Say>" \
                        "<Gather/>" \
                    "</Response>",
                headers={"Content-Type": "application/xml"})

        return twilio_webhook

    def prompt(self, text):
        return self.twiml("<Gather action='/webhooks/twilio_voice/action' input='speech' actionOnEmptyResult='true'>" \
                    "<Say>" + text + "</Say>" \
                "</Gather>")

    def twiml(self, text):
        return response.text("<Response>" + text + "</Response>",
            headers={"Content-Type": "application/xml"})
 