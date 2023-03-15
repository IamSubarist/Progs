from db import *
import datetime
from sqlalchemy import func

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import re

vk_session = vk_api.VkApi(token = 'vk1.a.ScxOIy07GDXBzQtQGpqd_8zCJ1Urm80Ww4Ldlz_9q7mnH8e9BLP7sEgJBy-4UfjFRDSJGUJy5ogiNNcbSTa_RCwTxuoQPOHG3dcnFCBpLCRNLoheWg--00WJeFjqDDMYsjGO7_k5Q3wH6hNfP5egLEmKauGOdzDROJZMpWpj-LaDT57sF_x0JYCS0AHezScH')
# 9e9b5d34217f5e5586c2cbf4fbe403b568f8d5d0e29fadf7ded47a54715ca8b1d6976380253d6c6023ba1 - основа
# dfb468c5cc7379cc98a8e697e4c2bd4fd2447cf12b7ceddc353e840ca13670fd95391d410ca3e130a0ea6 - тест
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
print('Бот запущен.')

def sender(user_id, text, keyboard=None):
    post = {
            'user_id' : user_id,
            'message' : text,
            'random_id' : 0,
        }
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        post = post

    vk_session.method('messages.send', post)

def flight():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id
            msg_update = msg.split()

            last_names = {
                        'Поперешняк': 'по',
                        'Просвиров': 'пр',
                        'Медный': 'м',
                        'Голозубов': 'г',
                        'Петренко': 'п',
                        'Чернышов': 'ч',
                        'Корчев': 'к',
                        'Цунаев': 'ц',
                        'Цвиров': 'цв',
                        'Ткаченко': 'т',
                    }
            
            def qwerty(arg):
                if len(arg) == 1:
                    for key, value in last_names.items():
                        value = value.split()
                        for i in value:
                            if arg[0] == i:
                                now = datetime.datetime.now()
                                today_date = now.strftime('%d-%m-%Y')

                                bunkers = Bunkers(user_id=user_id, bunkers=1, last_name=key, date=today_date)
                                session.add(bunkers)
                                session.commit()

                                sender(user_id, 'ОК!')

                                return
            
            if msg == 'бункеры за сегодня':
                now = datetime.datetime.now()
                today_date = now.strftime('%d-%m-%Y')

                message_bunkers = ''
                bunkerstotal = session.query(func.count(Bunkers.bunkers), Bunkers.last_name, Bunkers.date).filter(Bunkers.date == today_date).filter(Bunkers.user_id == user_id).group_by(Bunkers.last_name).all()
                bunkerscount = session.query(func.count(Bunkers.bunkers)).filter(Bunkers.date == today_date).filter(Bunkers.user_id == user_id)[0][0]
                for item in bunkerstotal:
                    message_bunkers += f'{item[1]} x {item[0]}\n'

                sender(user_id, f'Всего: {bunkerscount} бункеров.\n\n{message_bunkers}')

            if msg == 'бункеры с начала уборки':
                now = datetime.datetime.now()
                today_date = now.strftime('%d-%m-%Y')

                message_bunkers = ''
                bunkerstotal = session.query(func.count(Bunkers.bunkers), Bunkers.last_name, Bunkers.date).filter(Bunkers.user_id == user_id).group_by(Bunkers.last_name).all()
                bunkerscount = session.query(func.count(Bunkers.bunkers)).filter(Bunkers.user_id == user_id)[0][0]
                for item in bunkerstotal:
                    message_bunkers += f'{item[1]} x {item[0]}\n'

                sender(user_id, f'С начала уборки: {bunkerscount} бункеров.\n\n{message_bunkers}')
            
            if msg == 'клавиатура':
                keyboard = VkKeyboard()
                keyboard.add_button('Бункеры за сегодня')
                keyboard.add_line()
                keyboard.add_button('Бункеры с начала уборки')

                sender(user_id, 'ОК!', keyboard)
            
            if msg == 'начать':
                keyboard = VkKeyboard()
                keyboard.add_button('Бункеры за сегодня')
                keyboard.add_line()
                keyboard.add_button('Бункеры с начала уборки')

                sender(user_id, 'ОК!', keyboard)

            qwerty(msg_update)

if __name__ == '__main__':
    flight()