# -*- coding: utf-8 -*-

# BaiduBOT test file

__author__ = 'EagLB'

import os
from dotenv import load_dotenv
from urllib import request
import json
import sys
import random

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

print(API_KEY, SECRET_KEY)

{
    # def show_choose_confidence(action_list):
    #    #confidence_list = []
    #    ##show all response and confidence
    #    #for single_action in action_list:
    #    #    #confidence_list.append(single_action['confidence'])
    #    #    print(single_action['say'],single_action['confidence'])

    #    ##choose confidence for test
    #    #print('Choose one response(1~%d):' %(len(action_list)),end = ' ')
    #    #while True:
    #    #    try:
    #    #        choose_confidence = int(input())
    #    #        if (choose_confidence>=1 and choose_confidence<=len(action_list)):
    #    #            return action_list[choose_confidence-1]
    #    #        else: print('please input in the range(1~%d): ' %len(action_list),end = ' ')   #false handle
    #    #    except ValueError: print('please input integer: ',end = ' ')                       #false handle
    #    return  action_list[0]  #max confidence
}  # show_choose_confidence


def get_access_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
        API_KEY, SECRET_KEY)
    req = request.Request(host)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    with request.urlopen(req) as response:
        content = response.read()
    if (content):
        pycontent = json.loads(content.decode('utf-8'))
        access_token = pycontent['access_token']
        print('Get access_token successfully')
        return access_token


def get_bot_response(str_access_token, ask_data, type, botsession):
    url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + str_access_token
    # print(botsession)
    post_data = {
        "version": "2.0",
        "bot_id": "7411",
        "log_id": "1",
        "bot_session": botsession,
        "request": {
            "client_session": "{\"client_results\":\"\", \"candidate_options\":[]}",
            "bernard_level": '1',
            "user_id": "1",
            "query_info": {
                "type": type,
                "source": "KEYBOARD"},
            "query": ask_data}
    }
    encoded_data = json.dumps(post_data).encode('utf-8')
    headers = {'Contnet-Type': 'application/json'}

    req = request.Request(url, data=encoded_data, headers=headers)
    with request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
    print(result)

    # show bot response
    action = result['result']['response']['action_list'][0]
    #realaction = show_choose_confidence(action)
    print('\n小蜜:', action['say'], 'confidence:',
          action['confidence'], 'type:', action['type'])
    return result

# choose_option is not available now/waiting for baidu update


def choose_option(result):
    # show and choose the option if exist
    option_list = result['result']['response']['action_list'][0]['refine_detail']['option_list']
    interaction_id = result['result']['interaction_id']
    if(option_list != []):
        num = 0
        for option in option_list:
            num += 1
            print(num, option['option'])
        while True:
            try:
                option_result = int(
                    input('Choose your answer(1~%d): ' % (len(option_list))))
                if option_result >= 1 and option_result <= len(option_list):
                    break
                else:
                    print('please input in the range(1~%d): ' %
                          len(option_list), end=' ')  # false handle
            except ValueError:
                print('please input integer: ', end=' ')  # false handle
        return json.dumps({'event_name': 'CHOICE',
                           'interaction_id': interaction_id,
                           'index': str(option_result)})
    else:
        return ""


if __name__ == '__main__':
    access_token = get_access_token()
    lastbotsession = ""
    #option = ""
    while True:
        # if option == "":
        print('\n输入q退出', end=' ')
        data = input('User: ')
        data_type = "TEXT"
        # else:
        #    data = option
        #    data_type = "EVENT"
        if data == 'q':
            break
        response = get_bot_response(
            access_token, data, data_type, lastbotsession)
        lastbotsession = response['result']['bot_session']
        #option = choose_option(response)
