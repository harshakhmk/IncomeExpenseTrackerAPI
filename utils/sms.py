import os
from twilio.rest import Client
from pathlib import Path

# Your Account Sid and Auth Token from twilio.com/console
# All the account credantials are saved in .env file

account_sid = os.getenv("TWILIO_ACCOUNT_SID", None)
auth_token = os.getenv("TWILIO_AUTH_TOKEN", None)
IE_TEAM_MOBILE = os.getenv("IE_TEAM_MOBILE", None)


def send_sms(number, name, message):

    if account_sid is not None and auth_token is not None:
        client = Client(account_sid, auth_token)

        if IE_TEAM_MOBILE is not None:
            message = client.messages.create(
                body=message, from_=IE_TEAM_MOBILE, to=number
            )
    else:
        raise Exception("Account Credentials Not Found")
