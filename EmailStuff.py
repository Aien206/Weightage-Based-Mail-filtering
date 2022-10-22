import os
import pickle
from types import NoneType
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type
import re
import string


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
our_email = 'm.umerfarooq206@gmail.com'

def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
        print(messages)    
    return messages



    
         


        

        
                            
def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# get the Gmail API service
service = gmail_authenticate()


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)    




def parse_parts(service, parts, folder_name, message):
    """
    Utility function that parses the content of an email partition
    """
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(service, part.get("parts"), folder_name, message)
            if mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    text = urlsafe_b64decode(data).decode()
                    return text
            elif mimeType == "text/html":

                text = urlsafe_b64decode(data).decode()
                return text
                # if the email part is an HTML content
                # save the HTML file and optionally open it in the browser

                

    
                    

def read_message(service, message):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    CombString = ""
    has_subject = False
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
           
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                CombString = CombString + value
               # we print the From address
               # print("From:", value)
            if name.lower() == "to":
                CombString = CombString + value
                # we print the To address
                #print("To:", value)
            if name.lower() == "subject":
                CombString = CombString + value
                # make our boolean True, the email has "subject"
               # has_subject = True
                # make a directory with the name of the subject
                
                # we will also handle emails with the same subject name
                
                
                #print("Subject:", value)
            if name.lower() == "date":
                CombString = CombString + value
                # we print the date when the message was sent
                #print("Date:", value)
    
   
        
    text = parse_parts(service, parts, folder_name, message)
    if(type(text ) != NoneType):
        CombString = CombString + text
    
    res = re.sub('['+string.punctuation+']', '', CombString).split()
    
    return res
                                  
def EmailCollect():
    results = search_messages(service, "is:unread newer_than:1d")
    print(results)
    print(f"Found {len(results)} results.")
    Mails = []
    for msg in results:
        res = read_message(service, msg)
        Mails.append(res)
    
    return Mails, results   
    


Keyword =  ["Urgent", "assignment", "class", "postponed", "cancelled", "ASAP", "as soon as possible", "research", "project", "timing"]  

def DetWeight(res, messages):
    SequencedMail = []
    DMail = []
    maxval = -5
    for i in range(len(messages)):
        value =  set(res[i]).intersection(Keyword)
        print(value)
        DMail.append([messages[i], len(value)])
        
        
            
    SequencedMail = sorted(DMail, key=lambda x: x[1], reverse=True)
    FinalList = [i[0] for i in SequencedMail]
    #print(FinalList)
    return FinalList    

def PrintList(FinalList):
    if(len(FinalList) > 10):
        i = 0;
        while(i < 10):
            print("https://mail.google.com/mail/u/0/#inbox/" + str(FinalList[i]["id"]))
            i = i + 1;
    else:
        i = 0;
        while(i < len(FinalList)):
            print("https://mail.google.com/mail/u/0/#inbox/" + str(FinalList[i]["id"]))
            i = i + 1;
        
    
    
    return 0;
    



gmail_authenticate
res, messages = EmailCollect()
FinalList = DetWeight(res, messages)
PrintList(FinalList)

# get emails that match the query you specify

    
    






