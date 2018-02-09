#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
from subprocess import call
import vk_api

def auth_handler():
    key = input("Input a sms-code: ")
    remember_device = True
    return key, remember_device

try:
    vk = vk_api.VkApi(login = '89859639002', auth_handler = auth_handler)
    vk.auth()
except vk_api.exceptions.PasswordRequired:
    pswrd = raw_input("Please, input a password: ")
    vk = vk_api.VkApi(login = '89859639002', password = pswrd, auth_handler = auth_handler)
    vk.auth()


DAYS = {
    '1': 'Mon',
    '2': 'Tue',
    '3': 'Wed',
    '4': 'Thu',
    '5': 'Fri',
    '6': 'Sat',
    '0': 'Sun'
}

BRIEF = {
    # Формат xxxA, где xxx - день недели, А - Верх или Низ
    'MonT': u'''
            \r1 Пара: ПЯП -лекция- [ауд. 522]
            \r2 Пара: [Окошечко, в которое можно выйти]
            \r3 Пара: ОМВС -лаб- [ауд. 531]
            \r4 Пара: Теория информации -пр.з- [ауд. 224]''',
    'MonB': u'''
            \r1 Пара: ПЯП -пр.з- [ауд. 314]
            \r2 Пара: ЭЭиС -лаб- [ауд. ]
            \r3 Пара: Теория информации -лекция- [ауд. 301]''',
    'TueT': u'''
            \r1 Пара: ОМТМО -лаб- [ВЦ]
            \r2 Пара: ОМТМО -лекция- [ауд. 224]''',
    'TueB': u'''
            \r1 Пара: ОМТМО -пр.з- [ауд. 328]
            \r2 Пара: ОМТМО -лекция- [ауд. 224]
            \r3 Пара: Правоведение -пр.з- [ауд. 406]
            \r4 Пара: Правоведение -лекция- [ауд. 412а]''',
    'WedT': u'''
            \r1 Пара: СиАОД -пр.з- [ауд. 308]
            \r2 Пара: Социология -лекция- [ауд. 526]
            \r3 Пара: Физра''',
    'WedB': u'''
            \r1 Пара: СиАОД -лекция- [ауд. 301]
            \r2 Пара: СиАОД -лаб- [ауд. ]
            \r3 Пара: Физра''',
    'ThuT': u'''
            \r1 Пара: ОМВС -лекция- [ауд. 511]
            \r2 Пара: ЭЭиС -лекция- [ауд. 347]
            \r3 Пара: Социолоция -пр.з- [ауд. 404]
            \r4 Пара: Физра''',
    'ThuB': u'''
            \r2 Пара: ЭЭиС -лекция- [ауд. 347]
            \r3 Пара: ЭЭиС -пр.з- [ауд. 347]
            \r4 Пара: Физра''',
    'FriT': u'''
            \r3 Пара: Практика
            \r4 Пара: Практика''',
    'FriB': u'''
            \r3 Пара: Практика
            \r4 Пара: Практика''',
    'SatT': u'\n~~Выходной~~',
    'SatB': u'\n~~Выходной~~',
    'SunT': u'\n~~Выходной~~',
    'SunB': u'\n~~Выходной~~'
} 

def get_brief():
    # Проверяет день и час запроса
    weekday_now = int(time.strftime("%w"))
    top_week = (int(time.strftime("%W")) - 5)%2 # True(1) - Верхняя,False(0) - Нижняя
    hour = int(time.strftime("%H"))
    if weekday_now == 0 and hour > 15: 
        if top_week:
            top_week = 0
        else:
            top_week = 1     
    if weekday_now == 6 and hour > 15:
        next_day = 'Sun'
    elif hour > 15:
        next_day = DAYS[str(weekday_now+1)]
    else:
        next_day = DAYS[str(weekday_now)]
    if top_week:
        next_day += 'T'
    else:
        next_day += 'B'
    return u'Брифинг на завтра: ' + BRIEF[next_day]




def msg_notify(item):
    user = vk.method('users.get', {'user_ids':item[u'user_id']})[0]
    print "New message from: " + user[u'first_name'] + ' ' + user[u'last_name'] 

def is_link(msg):
    for domain in domains:
        if domain in msg:
            return True
    return False

def write_msg(user_id, s):
    vk.method('messages.send', {'user_id':user_id,'message':s})
def write_chat_msg(chat_id, s):
    vk.method('messages.send', {'chat_id':chat_id, 'message':s})

domains = ['.ru', '.com', '.net', 'http', 'www', '.org']

briefing_told = False
notify = False

# main loop
print "Bot is working"

VALUES = {'out': 1, 'count': 3, 'time_offset': 15} # настройки прочтения

while True:
    try:
        time.sleep(5)
        curr_time = time.strftime("%H:%M")
        if curr_time == "21:00":
            write_chat_msg(46,u"~Тестовый режим~\n"+get_brief())
            time.sleep(55)
        response = vk.method('messages.get', VALUES)
        if response['items']:
            VALUES['last_message_id'] = response['items'][0]['id']
        for item in response['items']:
            message_text = item[u'body'].lower()
            if notify:
                msg_notify(item)      
            if message_text == u'#брифинг':
                write_msg(item[u'user_id'], get_brief())
            if item[u'user_id'] == 91114313 and is_link(message_text):
                print "Got a link\nOpening...."
                call(["firefox", message_text])
    except vk_api.exceptions.ApiHttpError:
        print "Http Error: Gateway Timeout\nTrying to Reconnect...\n"
        vk.auth()
