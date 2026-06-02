import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from datetime import datetime, timedelta

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


def create_calendar_event():
    # get the Google credentials to authenticate
    creds = get_credentials()

    # build the Google Calendar service object
    service = build("calendar", "v3", credentials=creds)

    start = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=2)

    # define the calendar event details
    event = {
        "summary": "Study Session - Python & Neetcode",
        "description": "Programming in Python study session",
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": "America/Los_Angeles"
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "America/Los_Angeles"
        },
    }

    # insert the event into the primary Google Calendar
    service.events().insert(calendarId="primary", body=event).execute()


def main():
    # get today's day of the week as a number (Monday=0, Sunday=6)
    today = datetime.now().weekday()

    # only send reminder on Monday (0) or Sunday (6)
    if today == 0 or today == 6:
        send_email()
        create_calendar_event()
    else:
        print("No reminder needed today.")


# only run main() if this file is executed directly
if __name__ == "__main__":
    main()
