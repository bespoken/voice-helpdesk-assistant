# -*- coding: utf-8 -*-
import logging
from pydash import py_
from sanic import Blueprint, response

from rasa.core.channels import InputChannel
from rasa.core.channels import UserMessage
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

        return cls(
            credentials.get("account_sid"), credentials.get("auth_token")
        )

    def __init__(self, account_sid, auth_token, debug_mode=True):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.debug_mode = debug_mode
        self.last_response_by_user = {}

    def blueprint(self, on_new_message):
        twilio_webhook = Blueprint("twilio_webhook", __name__)

        @twilio_webhook.route("/", methods=["GET"])
        async def health(request):
            return response.json({"status": "ok"})

        @twilio_webhook.route("/webhook", methods=["POST"])
        async def message(request):
            print(request.form)  # The payload is form-encoded body
            call_sid = request.form.get("CallSid", None)
            out = CollectingOutputChannel()
            await on_new_message(
                UserMessage(
                    "Hello there", out, call_sid, input_channel="twilio_voice"
                )
            )

            return self.prompt(out.messages[0]["text"])

        @twilio_webhook.route("/action", methods=["POST"])
        async def action(request):
            print("/action called - form: " + str(request.form))
            result = request.form.get("SpeechResult")
            call_sid = request.form.get("CallSid", None)

            print("Result: " + str(result))

            if result:
                out = CollectingOutputChannel()

                # sends message to Rasa, wait for the response
                await on_new_message(
                    UserMessage(
                        result, out, call_sid, input_channel="twilio_voice"
                    )
                )

                # extract the text from Rasa's response
                last_response = py_.nth(out.messages, -1)

                # Some times on restarts, the server is in a weird state and their may be no session for an action
                if last_response:
                    print("last message: " + last_response["text"])
                    return self.prompt(last_response["text"])
                else:
                    return self.prompt('How can I help you today?')
            else:
                # If we did not get a user response, just reprompt
                return self.prompt("sorry, I did not get that - please repeat")

        return twilio_webhook

    def prompt(self, text):
        return self.twiml(
            "<Gather action='/webhooks/twilio_voice/action'"
            "        input='speech' speechTimeout='2'"
            "        actionOnEmptyResult='true'>"
            "     <Say>" + text + "</Say>"
            "</Gather>"
        )

    def twiml(self, text):
        return response.text(
            "<Response>" + text + "</Response>",
            headers={"Content-Type": "application/xml"},
        )
