from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import email
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']



def get_message(service, user_id, msg_id):

    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format="raw").execute()

        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('UTF-8'))

        msg_str = email.message_from_bytes(msg_raw)

        content_types = msg_str.get_content_maintype()

    
        return msg_str.get_payload()

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')



    
         

def search_messages(service, user_id, search_string):

    try:

        list_ids = []

        search_ids = service.users().messages().list(userId=user_id, q=search_string).execute()

        try:
            ids = search_ids["messages"]
        except KeyError:
            print("WARNING: the Search queried returned zero results")
            print("returning an empty string")
            return ""

        if len(ids)>1:
            for msg_id in ids:
                list_ids.append(msg_id['id'])
            return(list_ids)

    except:
        print("oopsies")
        # TODO(developer) - Handle errors from gmail API.
        
        

        
                            
def get_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build("gmail", 'v1', credentials=creds)

    return service

Exit = 0
if(Exit == 0):
    print("Welcome to the gmail message collection system")
    print("press 1 to enter the email collection")
    print("type 2 to quit the system")
    selection = input("enter:")
    if(selection == "1"):
        userid = input("enter user id")
        searchstring = input("enter search string")
        service = get_service()
        messagesearch = search_messages(service, userid, searchstring)
        for i in messagesearch:
            messages = get_message(service, userid, i)
            print(messages)
        





