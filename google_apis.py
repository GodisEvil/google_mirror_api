#!python
#-*-coding:utf-8-*-
'''
    
'''


from oauth2client import client
from googleapiclient import errors
from googleapiclient import discovery
import os
import json
from googleapiclient.http import MediaIoBaseUpload
import io
import httplib2


SCOPES = ['https://www.googleapis.com/auth/glass.timeline', 'https://www.googleapis.com/auth/userinfo.profile']
CREDENTIAL_DIR = 'credentials'

class GoogleApis():
    def __init__(self):
        self.credentials = {}
        if not os.path.exists(CREDENTIAL_DIR):
            os.makedirs(CREDENTIAL_DIR)
        else:
            for fname in os.listdir(CREDENTIAL_DIR):
                userid = fname
                with open(os.path.join(CREDENTIAL_DIR, fname), 'rb') as fp:
                    credential = json.load(fp)
                    credentials = client.OAuth2Credentials.from_json(credential)
                    if credentials.access_token_expired:
                        credentials.refresh(httplib2.Http())
                        # self.saveCredential(userid=userid, credentials=credentials)
                    self.credentials[userid] = credentials


    def getUsers(self):
        return self.credentials.keys()


    def getCredential(self, userid):
        return self.credentials.get(userid, None)


    def saveCredential(self, userid, credentials):
        with open(os.path.join(CREDENTIAL_DIR, userid), 'wb+') as fp:
            fp.write(json.dumps(credentials))
        credential = client.OAuth2Credentials.from_json(credentials)
        if credential.access_token_expired:
            credential.refresh(http=httplib2.Http())
        self.credentials[userid] = credential
        return True


    def listTimeline(self, userid):
        credential = self.credentials.get(userid, None)
        if not credential:
            return None
        # cred = credential.authorize(httplib2.Http())
        service = discovery.build('mirror', 'v1', credentials=credential)
        result = []
        request = service.timeline().list()
        while request:
            try:
                timeline_items = request.execute()
                items = timeline_items.get('items', [])
                if items:
                    result.extend(timeline_items.get('items', []))
                    request = service.timeline().list_next(request, timeline_items)
                else:
                    # No more items to retrieve.
                    break
            except errors.HttpError as error:
                print('An error occurred: %s' % error)
                break
        return result


    def insertTimeline(self, userid, contentType=None, attachMent=None, notificationLevel=None):
        '''
        https://stackoverflow.com/questions/16997932/attaching-video-with-video-vnd-google-glass-stream-url-after-update-xe6/16998808#16998808
        https://stackoverflow.com/questions/17621225/attaching-a-video-stream-through-the-net-mirror-api
        :return:
        '''
        credential = self.credentials.get(userid, None)
        if not credential:
            return False
        service = discovery.build('mirror', 'v1', credentials=credential)
        item = {'text': 'hello world'}
        mediaBody = None
        if notificationLevel:
            item['notification'] = {'level': notificationLevel}
        if contentType and attachMent:
            mediaBody = MediaIoBaseUpload(
                io.BytesIO(attachMent), mimetype=contentType, resumable=True)
        try:
            return service.timeline().insert(
                body = item, media_body = mediaBody
            ).execute()
        except errors.HttpError as error:
            print('error occurred: %s' % error)
            return False


    def getAccessToken(self, userid):
        credential = self.credentials.get(userid, None)
        if credential:
            return credential.access_token
        return None


    def getTimeline(self, userid, itemId):
        credential = self.credentials.get(userid, None)
        if credential:
            service = discovery.build('mirror', 'v1', credentials=credential)
            item_id = itemId
            # from apiclient import errors
            try:
                timeline_item = service.timeline().get(id=item_id).execute()

                print('Timeline item ID:  %s' % timeline_item.get('id'))
                if timeline_item.get('isDeleted'):
                    print('Timeline item has been deleted')
                else:
                    creator = timeline_item.get('creator')
                    if creator:
                        print('Timeline item created by  %s' % creator.get('displayName'))
                    print('Timeline item created on  %s' % timeline_item.get('created'))
                    print('Timeline item displayed on %s' % timeline_item.get('displayTime'))
                    in_reply_to = timeline_item.get('inReplyTo')
                    if in_reply_to:
                        print('Timeline item is a reply to  %s' % in_reply_to)
                    text = timeline_item.get('text')
                    if text:
                        print('Timeline item has text:  %s' % text)
                    for contact in timeline_item.get('recipients', []):
                        print('Timeline item is shared with:  %s' % contact.get('id'))
                    notification = timeline_item.get('notification')
                    if notification:
                        print('Notification delivery time: %s' % (
                            notification.get('deliveryTime')))
                        print('Notification level:  %s' % notification.get('level'))
                    menuItems = timeline_item.get('menuItems')
                    if menuItems:
                        print('menu action: %s' % menuItems.get('action'))
                        print('menu value: %s' % str(menuItems.get('values')))
                        print('menu payload: %s' % str(menuItems.get('payload')))
                    # See mirror.timeline.attachments.get to learn how to download the
                    # attachment's content.
                    for attachment in timeline_item.get('attachments', []):
                        print('Attachment ID: %s' % attachment.get('id'))
                        print('  > Content-Type: %s' % attachment.get('contentType'))
                        print('url: %s' % attachment.get('canonicalUrl'))
                    return timeline_item
            except errors.HttpError as error:
                print('An error occurred: %s' % error)


googleApis = GoogleApis()