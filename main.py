import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

SCOPES = ["https://www.googleapis.com/auth/gmail.send",
          "https://www.googleapis.com/auth/calendar"]


def get_credentials():
    creds = None

    # check if we already have a saved token from a previous login
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        # first time running open browser to log into Google
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

        # save the credentials so we don't have to log in again next time
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def send_email():
    # get the google credentials to authenticate
    creds = get_credentials()

    # guild the Gmail service object so we can interact with the Gmail API
    service = build("gmail", "v1", credentials=creds)

    # create the email message with the body text
    message = MIMEText(
        "Hey Marcos, don't forget you have a study session today! Time to grind some Python & NeetCode 💪")

    # Set the recipient and subject line
    message["to"] = "marcosperezdev16@gmail.com"
    message["subject"] = "Neo Hikari Study Session"

    # convert the message to base64 format that Gmail's API requires
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Wrap it in a dictionary as the request body
    body = {"raw": raw}

    # send the email via the Gmail API
    service.users().messages().send(userId="me", body=body).execute()
