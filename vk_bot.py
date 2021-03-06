#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import fileparsing
from subprocess import call
import vk_api

def auth_handler():
    key = input("Input a sms-code: ")
    remember_device = True
    return key, remember_device

try:
    login = raw_input("Input your email or number: ")
    vk = vk_api.VkApi(login = login, auth_handler = auth_handler)
    vk.auth()
except vk_api.exceptions.PasswordRequired:
    pswrd = raw_input("Please, input a password: ")
    vk = vk_api.VkApi(login = login, password = pswrd, auth_handler = auth_handler)
    vk.auth()

def write_msg(user_id, s):
    vk.method('messages.send', {'user_id':user_id,'message':s})
def write_chat_msg(chat_id, s):
    vk.method('messages.send', {'chat_id':chat_id, 'message':s})

# main loop
print "Bot is working"

#response = vk.method('messages.getConversations', {'offset':0,'count':1,'filter':'all'})


while True:
    try:
        time.sleep(15)
        curr_time = time.strftime("%H:%M")
        if curr_time == "20:00":
           write_chat_msg(61,"Брифинг на завтра:\n"+fileparsing.get_timetable()) 
           print "Timetable send"
           print fileparsing.get_timetable()
           time.sleep(55) 
    except vk_api.exceptions.ApiHttpError:
        print "Oops...Catch an error\nFixing..."
        vk.auth(reauth=True)
        print "Bot is working"