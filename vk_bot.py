# -*- coding: utf-8 -*-
import time
#import codecs
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
            1 Пара: ПЯП -лекция- [ауд. 522]
            2 Пара: ПЯП -пр.з- [ауд. 314]
            3 Пара: ОМВС -лаб- [ауд. 531]
            4 Пара: Теория информации -пр.з- [ауд. 224]
            ''',
    'MonB': u'''
            2 Пара: ЭЭиС -лаб- [ауд. ]
            3 Пара: Теория информации -лекция- [ауд. 301]
            ''',
    'TueT': u'''
            1 Пара: ОМТМО -лаб- [ВЦ]
            2 Пара: ОМТМО -лекция- [ауд. 224]
            ''',
    'TueB': u'''
            1 Пара: ОМТМО -пр.з- [ауд. 328]
            2 Пара: ОМТМО -лекция- [ауд. 224]
            3 Пара: Правоведение -пр.з- [ауд. 406]
            4 Пара: Правоведение -лекция- [ауд. 412а]
            ''',
    'WedT': u'''
            1 Пара: СиАОД -пр.з- [ауд. 308]
            2 Пара: Социология -лекция- [ауд. 526]
            3 Пара: Физра
            ''',
    'WedB': u'''
            1 Пара: СиАОД -лекция- [ауд. 301]
            2 Пара: СиАОД -лаб- [ауд. ]
            3 Пара: Физра
            ''',
    'ThuT': u'''
            1 Пара: ОМВС -лекция- [ауд. 511]
            2 Пара: ЭЭиС -лекция- [ауд. 347]
            3 Пара: Социолоция -пр.з- [ауд. 404]
            4 Пара: Физра
            ''',
    'ThuB': u'''
            2 Пара: ЭЭиС -лекция- [ауд. 347]
            3 Пара: ЭЭиС -пр.з- [ауд. 347]
            4 Пара: Физра
            ''',
    'FriT': u'''
            2 Пара: Практика
            3 Пара: Практика
            ''',
    'FriB': u'''
            2 Пара: Практика
            3 Пара: Практика
            ''',
    'SatT': u'\n~~Выходной~~',
    'SatB': u'\n~~Выходной~~',
    'SunT': u'\n~~Выходной~~',
    'SunB': u'\n~~Выходной~~'
} 

def get_brief():
    # Проверяет день и час запроса
    weekday_now = int(time.strftime("%w"))
    top_or_bot_week = (int(time.strftime("%W")) - 5)%2 # 1 - Верхняя, 0 - Нижняя
    hour = int(time.strftime("%H"))
    if weekday_now == 0 and hour > 15: 
        if top_or_bot_week == 1:
            top_or_bot_week = 0
        else:
            top_or_bot_week = 1     
    if weekday_now == 6 and hour > 15:
        next_day = 'Sun'
    elif hour > 15:
        next_day = DAYS[str(weekday_now+1)]
    elif hour < 9:
        next_day = DAYS[str(weekday_now)]
    else: 
        return u"Еще рановато"
    if top_or_bot_week:
        next_day += 'T'
    else:
        next_day += 'B'
    return u'Брифинг на завтра: ' + BRIEF[next_day]

VALUES = {'out': 1, 'count': 3, 'time_offset': 15}

def write_msg(user_id, s):
    vk.method('messages.send', {'user_id':user_id,'message':s})
def write_chat_msg(chat_id, s):
    vk.method('messages.send', {'chat_id':chat_id, 'message':s})

domains = ['.ru', '.com', '.net', 'http', 'www', '.org']

briefing_told = False

while True:
    try:
        curr_hour = int(time.strftime("%H"))
        curr_min = int(time.strftime("%M"))
        if curr_hour == 19 and curr_min == 0 and not briefing_told:
            write_chat_msg(46,"~Тестовый режим~\n"+get_brief())
            briefing_told = True
        elif curr_hour != 19 and curr_min != 0:
            briefing_told = False
        response = vk.method('messages.get', VALUES)
        if response['items']:
            VALUES['last_message_id'] = response['items'][0]['id']
        for item in response['items']:
            message_text = item[u'body'].lower()
            print str(item[u'user_id']) + ': ' + item[u'body']
            if message_text == u'#брифинг':
                write_msg(item[u'user_id'], get_brief())
            elif item[u'user_id'] == 91114313:
                for domain in domains:
                    if domain in message_text:
                        call(["firefox", message_text])
                        break
        time.sleep(10)
    except vk_api.exceptions.ApiHttpError:
        print "Http Error: Gateway Timeout\nTrying to Reconnect...\n"
        vk.auth()