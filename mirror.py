#!python
#-*-coding:utf-8-*-
'''
    google mirror
    https://developers.google.com/api-client-library/python/auth/web-app
        flow = client.flow_from_clientsecrets(...)
        flow.params['access_type'] = 'offline'
    https://stackoverflow.com/questions/27771324/google-api-getting-credentials-from-refresh-token-with-oauth2client-client

    https://stackoverflow.com/questions/21103275/call-python-quickstart-mirror-api-remotely

    https://developers.google.com/glass/v1/reference/timeline/list
'''


from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
from oauth2client import client


import json
import time
import flask
from flask import request
import requests
import urllib
import os
from google_apis import googleApis


SCOPES = ['https://www.googleapis.com/auth/glass.timeline', 'https://www.googleapis.com/auth/userinfo.profile']
CREDENTIAL_DIR = 'credentials'
app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.redirect(flask.url_for('listTimeline'))


@app.route('/timeline/list')
def listTimeline():
    userid = request.args.get('userid', '')
    if not userid:
        return flask.redirect(flask.url_for('oauth2callback'))
    ret = {'code': 0, 'data': googleApis.listTimeline(userid)}
    return json.dumps(ret)


@app.route('/timeline/insert', methods=['GET', 'POST'])
def insertTimeline():
    '''
    Using the access_token query parameter like this: ?access_token=oauth2-token
    Using the HTTP Authorization header like this: Authorization: Bearer oauth2-token
    :return:
    '''
    userid = request.args.get('userid', '')
    videoUrl = request.args.get('url', '')
    if not userid or not videoUrl:
        return json.dumps({'code': 2, 'msg': 'need userid and url'})
    ## 直接把 post 的记录 post 到服务器,但是加上一个头 Authorization
    # return json.dumps(googleApis.insertTimeline(userid=userid))
    accessToken = googleApis.getAccessToken(userid)
    if not accessToken:
        return json.dumps({'code': 1, 'msg': 'user is not valid'})
    headers = {}
    # for i in request.headers.keys():
    #     headers[i] = request.headers.get(i)
    headers['Authorization'] = 'Bearer %s' % accessToken
    headers['Content-Type'] = 'application/json'
    body = {'text': 'Hello world', 'menuItems': [{'action': 'PLAY_VIDEO', 'payload': videoUrl, 'id': 'video_' + str(time.time())}]}
    body = bytes(json.dumps(body))
    headers['Content-Length'] = str(len(body))
    ret = requests.post(url = 'https://www.googleapis.com/mirror/v1/timeline', data=body, headers = headers)
    for i in headers:
        print(i)
        print(headers[i])
    print (body)
    print (ret.status_code)
    return ret.text


@app.route('/timeline/video', methods=['GET', 'POST'])
def addTimelineVideo():
    '''
    Using the access_token query parameter like this: ?access_token=oauth2-token
    Using the HTTP Authorization header like this: Authorization: Bearer oauth2-token
    :return:
    '''
    userid = request.args.get('userid', '')
    videoUrl = request.args.get('url', '')
    if not userid or not videoUrl:
        return json.dumps({'code': 2, 'msg': 'need userid and url'})
    ## 直接把 post 的记录 post 到服务器,但是加上一个头 Authorization
    # return json.dumps(googleApis.insertTimeline(userid=userid))
    accessToken = googleApis.getAccessToken(userid)
    if not accessToken:
        return json.dumps({'code': 1, 'msg': 'user is not valid'})
    headers = {}
    # for i in request.headers.keys():
    #     headers[i] = request.headers.get(i)
    headers['Authorization'] = 'Bearer %s' % accessToken
    headers['Content-Type'] = 'multipart/related; boundary="mymultipartboundary"'
    body = '--mymultipartboundary\r\n' \
        'Content-Type: application/json; charset=UTF-8\r\n\r\n' \
        '{ "text": "Sweetie" }\r\n' \
        '--mymultipartboundary\r\n' \
        'Content-Type: video/vnd.google-glass.stream-url\r\n\r\n'\
        '%s\r\n' \
        '--mymultipartboundary--\r\n' % videoUrl
    body = bytes(body)
    headers['Content-Length'] = str(len(body))
    ret = requests.post(url = 'https://www.googleapis.com/upload/mirror/v1/timeline', data=body, headers = headers)
    for i in headers:
        print(i)
        print(headers[i])
    print (body)
    print (ret.status_code)
    return ret.text


@app.route('/timeline/get')
def getTimeline():
    '''
    get special tiemline item
    :return:
    '''
    userid = request.args.get('userid', '')
    itemid = request.args.get('itemid', '')
    ret = googleApis.getTimeline(userid=userid, itemId=itemid)
    return json.dumps({'code': 0, 'data': ret})


@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope=SCOPES,
      redirect_uri=flask.url_for('oauth2callback', _external=True))
      # include_granted_scopes=True)
  ## 允许离线访问
  flow.params['access_type'] = 'offline'
  # flow.params['include_granted_scopes'] = True
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    credentials = credentials.to_json()
    credential = json.loads(credentials)
    tokenInfo = credential['token_response']
    access_token = tokenInfo['access_token']
    r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + access_token)
    if r.status_code == requests.codes.ok:
        userInfo = r.json()
        googleApis.saveCredential(userInfo['id'], credentials)
        return flask.redirect(flask.url_for('listTimeline', userid = urllib.quote(userInfo['id'])))
    else:
        return json.dumps({'code': 1, 'msg': 'get userinfo failed'})


@app.route('/timeline/info')
def infoTimeline():
    '''

    :return:
    '''
    userid = request.args.get('userid', '')
    url = request.args.get('url', '')
    if not userid or not url:
        return json.dumps({'code': 1, 'msg': 'need userid, itemid'})
    token = googleApis.getAccessToken(userid)
    # url = 'https://www.googleapis.com/mirror/v1/timeline/' + itemid
    ret = requests.get(url=url, headers = {'Authorization': 'Bearer ' + token})
    print(ret.status_code)
    return json.dumps({'code': 0, 'data': ret.text})


if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  if not os.path.exists(CREDENTIAL_DIR):
      os.makedirs(CREDENTIAL_DIR)
  server = WSGIServer(('0.0.0.0', 5000), app)
  server.serve_forever()

