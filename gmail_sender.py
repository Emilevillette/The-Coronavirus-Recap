from __future__ import print_function

import base64
import os
from email.mime.text import MIMEText

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def send_email(sender, recipient, subject, content):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'User_data/OAUTH2/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    message = create_message(sender, recipient, subject, content)
    print(send_message(service, "me", message))
    # Call the Gmail API


def create_message(sender, to, subject, message_text):
    """Create a message for an emaildata.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the emaildata message.
      message_text: The text of the emaildata message.

    Returns:
      An object containing a base64url encoded emaildata object.
    """
    message = MIMEText(message_text, "html")
    message['to'] = to
    message['subject'] = subject
    print(type(message))
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service, user_id, message):
    """Send an emaildata message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's emaildata address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print('An error occurred: %s' % error)
