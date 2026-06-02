import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

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
