import os
import json
import time
import base64
import facebook
import requests
import datetime
import httplib2
import mimetypes
import fb_config as fc
from apiclient import errors
from oauth2client import tools
from apiclient import discovery
from oauth2client import client
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from oauth2client.file import Storage
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

## ---------------------------------------- Config Section ---------------------------------------- ##

FACEBOOK_GRAPH_URL = "https://graph.facebook.com/"
access_token = fc.access_token
long_lived_token = fc.long_lived_token
appid = fc.appid
appsecret = fc.appsecret
SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
CLIENT_SECRET_FILE = fc.filepath
APPLICATION_NAME = fc.appname
home_dir = fc.dir_path

## -------------------------------------- End Config Section -------------------------------------- ##

def get_cred():
    # home_dir = os.path.expanduser()
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')

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
def CreateMessage(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def gmail_send_msg(user_id, msg):
    '''
    Send email to given email (Or the list of emails) to notify the user
    '''
    credentials = get_cred()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message = CreateMessage('me','akashk@arista.com','[Facebook Notification]',msg)
    try:
        message = (service.users().messages().send(userId='me', body=message).execute())
        print 'Message Id: %s' % message['id']
        return message
    except errors.HttpError, error:
        print 'An error occurred: %s' % error

def get_token():
    '''
    To generate long lived facebook access token.
    '''
    fb = facebook.GraphAPI(access_token)
    token = fb.extend_access_token(appid, appsecret)
    return token['access_token']

if __name__ == '__main__':
    st_time = datetime.datetime.utcnow().isoformat()
    graph = facebook.GraphAPI(long_lived_token)
    # This loop will continuously check for new posts on group after every 5 seconds.
    while True:
        feed = graph.get_object('746844162121794',fields = 'feed,updated_time')
        latest_post_id = feed['feed']['data'][0]['id']
        curr_mod_date = feed['feed']['data'][0]['updated_time']
        if curr_mod_date > st_time:
            st_time = curr_mod_date
            post = graph.get_object(latest_post_id, fields = 'message,comments')
            message = []
            if 'comments' in post:
                message.append("Post : " + str(post['message']))
                l = len(post['comments']['data'])
                comment = post['comments']['data'][-1]
                message.append("Last Comment by " + str(comment['from']['name']) + " : " +str(comment['message']))
                msg = "\n".join(message)
                gmail_send_msg('akashk@arista.com',msg)
                print 'Change Detected'
                print msg
            else:
                message.append("Post : " + str(post['message']))
                msg = "\n".join(message)
                msg = "\n".join(message)
                gmail_send_msg('akashk@arista.com',msg)
                print 'Change Detected'
                print msg
        else:
            print 'No change'
        time.sleep(5.0)
