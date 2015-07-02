import codecs
import json
import os
import random
import requests
import time
import yaml

TOKEN = ""
URL = "https://api.telegram.org/bot" + TOKEN

def getData():
    data = json.loads(requests.post(URL + "/getUpdates").text)
    result = data['result']
    return result

def getLatestDate():
    result = getData()
    date = result[len(result)-1]['message']['date']
    return date

def getUpdates():
    result = getData()
    res_len = len(result)-1
    chat_id = result[res_len]['message']['chat']['id']
    user_id = result[len(result)-1]['message']['from']['id']
    msg_id = result[res_len]['message']['message_id']
    user_name = result[res_len]['message']['from']['first_name']
    text = result[res_len]['message']['text']
    if(text.startswith('/')):
        if(text.startswith('/waifu')):
            with open('~/WaifuBot/waifu.yml', 'r') as f:
                waifu = yaml.load(f)
            waifu_text = random.choice(list(waifu.keys()))
            waifu_title = waifu[waifu_text][0]
            try:
                image = 'Images/' + waifu_title +'/' + waifu_text + '.png'
                files = {'photo': (image, open(image, "rb"))}
                data = {'chat_id': chat_id, 'reply_to_message_id': msg_id, 'caption': user_name + '\'s waifu is ' + waifu_text + ' (' + waifu_title + ')'}
                status = requests.post(URL + "/sendPhoto", data=data, files=files)
            except OSError:
                params = {'chat_id': chat_id, 'reply_to_message_id': msg_id, 'text': user_name + '\'s waifu is ' + waifu_text + ' (' + waifu_title + ')'}
                status = requests.post(URL + "/sendMessage", params=params)
        elif(text.startswith('/shipgirl')):
            with open('~/WaifuBot/shipgirl.yml', 'r') as f:
                waifu = yaml.load(f)
            waifu_text = random.choice(list(waifu.keys()))
            waifu_title = waifu[waifu_text][0]
            try:
                image = 'Images/' + waifu_title +'/' + waifu_text + '.png'
                files = {'photo': (image, open(image, "rb"))}
                data = {'chat_id': chat_id, 'reply_to_message_id': msg_id, 'caption': user_name + '\'s shipgirl is ' + waifu_text + ' (' + waifu_title + ')'}
                status = requests.post(URL + "/sendPhoto", data=data, files=files)
            except OSError:
                params = {'chat_id': chat_id, 'reply_to_message_id': msg_id, 'text': user_name + '\'s shipgirl is ' + waifu_text + ' (' + waifu_title + ')'}
                status = requests.post(URL + "/sendMessage", params=params)
    return res_len

result_length = 0
current_reslen = len(getData()) - 1

while True:
    if(result_length != current_reslen):
        current_reslen = getUpdates()
        result_length = current_reslen
    time.sleep(1)
    current_reslen = len(getData())-1
    
    
