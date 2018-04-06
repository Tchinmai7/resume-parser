from __future__ import print_function
import httplib2
import os
import pprint
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'cs.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getMail():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().messages().list(userId='me').execute()
    emails = []
    for result in results['messages']:
        email_content = service.users().messages().get(userId='me', id=result['id']).execute()
        emails.append(email_content)
    # clean and return only required fields
    # for now: subject, snippet, body and attachments
    r_emails = []
    for each in emails:
        r_email = {}
        for header in each['payload']['headers']:
            if header['name'] == 'Subject':
                r_email['subject'] = header['value']
        r_email['body_snippet'] = each['snippet']
        r_email['attachments'] = []
        r_email['body'] = []
        for part in each['payload']['parts']:
            if 'body' in part and 'attachmentId' in part['body']:
                r_email['attachments'].append(part)
            if 'body' in part and 'data' in part['body']:
                r_email['body'].append(part)
        r_emails.append(r_email)
    return r_emails
