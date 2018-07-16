#-*- coding: utf-8 -*-

'BaiduBOT test file'

__author__ = 'EagLB'

from urllib import request
import json
import sys
import random

#API_KEY and SEVRET_KEY are authorized from Baidu.

def show_choose_confidence(action_list):
    confidence_list = []
    #show all response and confidence
    for single_action in action_list:
        #confidence_list.append(single_action['confidence'])
        print(single_action['say'],'\n',single_action['confidence'])

    ##choose confidence for test
    #print('Choose one response(1~%d):' %(len(action_list)),end = ' ')
    #while True:
    #    try:
    #        choose_confidence = int(input())
    #        if (choose_confidence>=1 and choose_confidence<=len(action_list)): 
    #            return action_list[choose_confidence-1]
    #        else: print('please input in the range(1~%d): ' %len(action_list),end = ' ')   #false handle
    #    except ValueError: print('please input integer: ',end = ' ')                       #false handle

    #max confidence
    return  action_list[0]  

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

def get_bot_response(str_access_token, ask_data, botsession):
    url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + str_access_token
    print(botsession)
    post_data = {
        "version": "2.0",
        "bot_id":"7411",
        "log_id":"1",
        "bot_session": botsession,
        "request":{
            "client_session":"{\"client_results\":\"\", \"candidate_options\":[]}",
            "bernard_level":'1',
            "user_id":"1",
            "query_info":{
                "type": "TEXT",
                "source":"KEYBOARD"},
            "query": ask_data}
        }
    encoded_data = json.dumps(post_data).encode('utf-8')
    headers = {'Contnet-Type': 'application/json'}

    req = request.Request(url, data = encoded_data, headers = headers)
    with request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))

    action = result['result']['response']['action_list']
    realaction = show_choose_confidence(action)
    print('\n小蜜:', realaction['say'],'confidence:',realaction['confidence'],'type:',realaction['type'] )  
    return result


if __name__ == '__main__':
    access_token = get_access_token()
    lastbotsession = ""
    while True:
        print('\n输入q退出',end = ' ')
        data = input('User: ')
        if data == 'q': break
        response = get_bot_response(access_token, data,lastbotsession)
        lastbotsession = response['result']['bot_session']








