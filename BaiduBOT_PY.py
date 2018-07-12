#-*- coding: utf-8 -*-

'BaiduBOT test file'

__author__ = 'EagLB'

from urllib import request
import json
import sys

#API_KEY and SEVRET_KEY are authorized from Baidu.


def get_access_token():
    #host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=API_KEY&client_secret=SECRET_KEY'
    req = request.Request(host)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    with request.urlopen(req) as response:
        content = response.read()
    if (content):
        pycontent = json.loads(content.decode('utf-8'))
        access_token = pycontent['access_token']
        print('Get access_token successfully')
        return access_token

def get_bot_response(str_access_token):
    url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + str_access_token
    post_data = {
        "version": "2.0",
        "bot_id":"5",
        "log_id":"122333",
        "bot_session":"",
        "request":{
            "client_session":"{\"client_results\":\"\", \"candidate_options\":[]}",
            "bernard_level":'1',
            "user_id":"122333",
            "query_info":{
                "type": "TEXT",
                "source":"KEYBOARD"},
            "query": "Hello"}  #your words
        }
    encoded_data = json.dumps(post_data).encode('utf-8')
    headers = {'Contnet-Type': 'application/json'}

    req = request.Request(url, data = encoded_data, headers = headers)
    with request.urlopen(req) as response:
        content = response.read()
    result = json.loads(content.decode('utf-8'))
    print(result['result']['response']['action_list'][3]['say'])




if __name__ == '__main__':
    get_bot_response(get_access_token())









