from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from urllib.error import HTTPError
import base64
import sys
import PySimpleGUI as psg

"""
This script allows the user to import or insert an encoded raw email in a Gmail account.
For reference: 
- insert method: https://developers.google.com/gmail/api/reference/rest/v1/users.messages/insert
- import method: https://developers.google.com/gmail/api/reference/rest/v1/users.messages/import

insert directly inserts a message into only this user's mailbox similar to IMAP APPEND, 
    bypassing most scanning and classification. Does not send a message. 
import doesn't trigger forwarding rules or filters set up by the user.
"""

"""
TODO:
    - implement case when email text is pasted on the input field (only browse
      working now)
"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.insert']

# Encode message in base64_urlsafe
def encodeMessage(filePath):
    data = open(filePath, 'r')
    encodedBytes = base64.urlsafe_b64encode(data.read().encode('utf-8'))
    message = str(encodedBytes, 'utf-8')
    # return the obj to be used in the request body for the api call    
    return {'raw': message}

# insert/import call to gmail api
def importOrInsertEmail(action, service, filePath):
    print('Please wait...')
    try:
        if action == 'Import':
            # execute import call
            service.users().messages().import_(userId='me', body=encodeMessage(filePath)).execute()
            print('successful import')
        elif action == 'Insert':
            service.users().messages().insert(userId='me', body=encodeMessage(filePath)).execute()
            print('successful insert')
    except HTTPError as error:
        print('An error ocurred: %s' % error) 

# Set everything related to the GUI and create the window
def setGUI(service):
    psg.theme('DarkAmber')
    # All the stuff inside the window
    layout = [ [psg.Text('Paste raw email text or browse the .eml/.txt file')],
              [psg.InputText(key='input'), psg.FileBrowse(target='input')],
              [psg.Button('Import'), psg.Button('Insert'), psg.Button('Close')] ]
    # create Window
    window = psg.Window('Import or Insert Email', layout)
    # Even Loop to process 'events' and get the 'value' of the input
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED or event == 'Close':
            break
        importOrInsertEmail(event, service, values['Browse'])

    window.close()

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    setGUI(service)

if __name__ == '__main__':
    main()

