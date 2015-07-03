# complete rewrite using pyTelegramBotAPI wrapper

import telebot
import time
import codecs
import json
import os
import random
import yaml
from urllib import request
from io import BytesIO
from PIL import Image
from booru import getImage

TOKEN = ''

def listener(*messages):
	for m in messages:
		chatid = m.chat.id
		if m.content_type == 'text':
			text = m.text
			name = m.fromUser.first_name
			msgid = m.message_id
			if(text.startswith('/')):
				if(text.startswith('/waifu')):
					with open('waifu.yml', 'r') as f:
						waifu = yaml.load(f)
						waifu_text = random.choice(list(waifu.keys()))
						waifu_title = waifu[waifu_text][0]
						print(name + ": " + waifu_text + " (" + waifu_title + ")")
						try:
							image = 'Images/' + waifu_title +'/' + waifu_text + '.png'
							photo = open(image, 'rb')
							tb.send_chat_action(chatid, 'upload_photo')
							tb.send_photo(chatid, photo, caption=name + '\'s waifu is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)
						except OSError:
							try:
								# tb.send_message(chatid, text=name + '\'s shipgirl is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)
								url = getImage(waifu_text.replace(" ", "_"))
								image = Image.open(BytesIO(request.urlopen(url).read())) 
								resized = image.resize((423, 586), Image.ANTIALIAS)
								out = BytesIO()
								resized.save(out,'PNG')
								imgfile = 'temp' + str(random.randint(0,100)) + '.png'
								f = open(imgfile,'wb')
								f.write(out.getvalue())
								f.close()
								img = open(imgfile, 'rb')
								tb.send_chat_action(chatid, 'upload_photo')
								tb.send_photo(chatid, img, caption=name + '\'s waifu is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)
								f.close()
								os.remove(imgfile)
							except AttributeError:
								tb.send_message(chatid, text=name + '\'s waifu is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)	
				elif text.startswith('/shipgirl'):
					with open('shipgirl.yml', 'r') as f:
						waifu = yaml.load(f)
						waifu_text = random.choice(list(waifu.keys()))
						waifu_title = waifu[waifu_text][0]
						try:
							print(name + ": " + waifu_text + " (" + waifu_title + ")")
							image = 'Images/' + waifu_title +'/' + waifu_text + '.png'
							photo = open(image, 'rb')
							tb.send_chat_action(chatid, 'upload_photo')
							tb.send_photo(chatid, photo, caption=name + '\'s shipgirl is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)
						except OSError:
							tb.send_message(chatid, text=name + '\'s shipgirl is ' + waifu_text + ' (' + waifu_title + ')', reply_to_message_id=msgid)
								
tb = telebot.TeleBot(TOKEN)
tb.get_update()  # cache exist message
tb.set_update_listener(listener) #register listener
tb.polling()
while True:
	time.sleep(1)