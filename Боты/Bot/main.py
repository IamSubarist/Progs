from db import *
from datetime import date, timedelta
import datetime
from sqlalchemy import func

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import re

vk_session = vk_api.VkApi(token = '9e9b5d34217f5e5586c2cbf4fbe403b568f8d5d0e29fadf7ded47a54715ca8b1d6976380253d6c6023ba1')
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

def tonnesinday():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id

            tonnes = Tonnes(user_id=user_id, tonnes=msg)
            session.add(tonnes)
            session.commit()
            sender(user_id, 'OK!')

            return flight()

def kilometersinday():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id

            kilometers = Kilometers(user_id=user_id, kilometers=msg)
            session.add(kilometers)
            session.commit()
            sender(user_id, 'OK!')

            return flight()

def flightsinday():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id

            flightsinday = Flightsinday(user_id=user_id, flightsinday=msg)
            session.add(flightsinday)
            session.commit()
            sender(user_id, 'OK!')

            return flight()

def flight():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id
            msg_update = msg.split()

            last_names = {
                        'Мелащенко_А.': 'ма мж',
                        'Мелащенко_В.': 'мв',
                        'Яцун': 'яцун я яц яцу',
                        'Осадчий': 'осачий осадчий асачий асадчий о ос оса',
                        'Редкоус': 'федорович фёдорович редкаус редкоус ридкаус ридкоус р ре ред',
                        'Бабичев': 'бабич бабичев б ба баб',
                        'Мухтаров': 'шамиль шомиль муха мухтаров м му мух',
                        'Петров': 'петров питров п пе пет',
                        'Задорожний': 'задорожний задарожний зодарожний з за зад',
                        'Финагеев': 'финагей финагеев фенагеев ф фи фин',
                        'Лаптин': 'лапть лаптин л ла лап',
                        'Трегубов': 'тригуб трегуб трегубов тригубов т тр тре',
                        'Цунаев': 'цунай цунаев ц цу цун',
                    }

            def qwerty(arg):
                keyboard = VkKeyboard()
                keyboard.add_button('Завершить рейс')
                keyboard.add_line()
                keyboard.add_button('Тонны за сегодня')
                keyboard.add_button('Километры за сегодня')
                keyboard.add_line()
                keyboard.add_button('Рейсы за сегодня')
                keyboard.add_line()
                keyboard.add_button('Бункеры за сегодня')
                keyboard.add_button('Бункеры за вчера')
                keyboard.add_line()
                keyboard.add_button('Формула')
                keyboard.add_line()
                keyboard.add_button('Статистика')

                argup = re.split('[: /]', arg[0])
                if len(argup) == 4:
                    formula = 0.01 * (33.5 * float(argup[0]) + 1.3 * float(argup[1]) * float(argup[2])) * (1 + 0.01 * 40) + (0.5 * float(argup[3]))
                    sender(user_id, f'0.01 * (33.5 * {argup[0]} + 1.3 * {argup[1]} * {argup[2]}) * (1 + 0.01 * 40) + (0.5 * {argup[3]})\n\n{round(formula, 1)}')

                elif len(arg) == 2:
                    if arg[1] == 'последний':
                        for key, value in last_names.items():
                            value = value.split()
                            for i in value:
                                if arg[0] == i:
                                    now = datetime.datetime.now()
                                    today_date = now.strftime('%d-%m-%Y')

                                    flight = Flight(flight_number=1, user_id=user_id, last_name=key)
                                    flights = Flights(user_id=user_id, flights=1, last_name=key, date=today_date)
                                    session.add(flight)
                                    session.add(flights)
                                    session.commit()

                        last_name = session.query(Flight.last_name).filter(Flight.user_id == user_id)
                        message = ''

                        for item in last_name:
                            num = session.query(Flight.last_name, func.count(Flight.flight_number)).filter(Flight.last_name == item[0]).filter(Flight.user_id == user_id)
                            message += f'{num[0][0]} '

                        splits = message.split()
                        sets = list(set(splits))

                        messages = ''
                        for item in sets:
                            query = session.query(func.count(Flight.flight_number)).filter(Flight.last_name == item).filter(Flight.user_id == user_id)
                            date = session.query(Flight.date).filter(Flight.user_id == user_id)[0]
                            messages += f'{item} x {query[0][0]}\n'

                        sender(user_id, f'{date[0]}\n\n{messages}')

                        total = session.query(Flight)
                        for item in total:
                            session.delete(item)
                            session.commit()

                elif len(arg) == 1:
                    for key, value in last_names.items():
                        value = value.split()
                        for i in value:
                            if arg[0] == i:
                                now = datetime.datetime.now()
                                today_date = now.strftime('%d-%m-%Y')

                                flight = Flight(flight_number=1, user_id=user_id, last_name=key, date=today_date)
                                flights = Flights(user_id=user_id, flights=1, last_name=key, date=today_date)
                                session.add(flight)
                                session.add(flights)
                                session.commit()

                                # tonnes = Tonnes(user_id=user_id, tonnes=0)
                                # session.add(tonnes)
                                # session.commit()

                                # kilometers = Kilometers(user_id=user_id, kilometers=0)
                                # session.add(kilometers)
                                # session.commit()

                                # flightsinday = Flightsinday(user_id=user_id, flightsinday=0)
                                # session.add(flightsinday)
                                # session.commit()

                                sender(user_id, 'ОК!', keyboard)

                                return

            if msg == 'завершить рейс':
                last_name = session.query(Flight.last_name).filter(Flight.user_id == user_id)
                message = ''

                for item in last_name:
                    num = session.query(Flight.last_name, func.count(Flight.flight_number)).filter(Flight.last_name == item[0]).filter(Flight.user_id == user_id)
                    message += f'{num[0][0]} '

                splits = message.split()
                sets = list(set(splits))

                messages = ''
                for item in sets:
                    query = session.query(func.count(Flight.flight_number)).filter(Flight.last_name == item).filter(Flight.user_id == user_id)
                    date = session.query(Flight.date).filter(Flight.user_id == user_id)[0]
                    messages += f'{item} x {query[0][0]}\n'

                sender(user_id, f'{date[0]}\n\n{messages}')

                total = session.query(Flight)
                for item in total:
                    session.delete(item)
                    session.commit()

            if msg == 'тонны за сегодня':
                sender(user_id, 'Сколько тонн за сегодня?\nВведите число:\nЕсли кнопка была нажата случайно, отправьте 0')
                tonnesinday()

            if msg == 'километры за сегодня':
                sender(user_id, 'Сколько километров за сегодня?\nВведите число:\nЕсли кнопка была нажата случайно, отправьте 0')
                kilometersinday()

            if msg == 'рейсы за сегодня':
                sender(user_id, 'Сколько рейсов за сегодня?\nВведите число:\nЕсли кнопка была нажата случайно, отправьте 0')
                flightsinday()

            if msg == 'бункеры за сегодня':
                now = datetime.datetime.now()
                today_date = now.strftime('%d-%m-%Y')
                
                message_bunkers = ''
                bunkersindaytotal = session.query(func.count(Flights.flights)).filter(Flights.date == today_date).filter(Flights.user_id == user_id)[0][0]
                bunkerstotal = session.query(func.count(Flights.flights), Flights.last_name, Flights.date).filter(Flights.date == today_date).filter(Flights.user_id == user_id).group_by(Flights.last_name).all()
                for item in bunkerstotal:
                    message_bunkers += f'{item[1]} x {item[0]}\n'

                sender(user_id, f'За сегодня: {bunkersindaytotal} бункеров.\n{message_bunkers}')

            if msg == 'бункеры за вчера':
                now = datetime.datetime.now()
                back_date_d = int(now.strftime('%d'))
                back_date_mY = now.strftime('-%m-%Y')
                back_date = f'{back_date_d - 1}{back_date_mY}'
                
                message_bunkers = ''
                bunkersindaytotal = session.query(func.count(Flights.flights)).filter(Flights.date == back_date).filter(Flights.user_id == user_id)[0][0]
                bunkerstotal = session.query(func.count(Flights.flights), Flights.last_name, Flights.date).filter(Flights.date == back_date).filter(Flights.user_id == user_id).group_by(Flights.last_name).all()
                for item in bunkerstotal:
                    message_bunkers += f'{item[1]} x {item[0]}\n'

                sender(user_id, f'За вчера: {bunkersindaytotal} бункеров.\n{message_bunkers}')

            if msg == 'админ':
                now = datetime.datetime.now()
                today_date = now.strftime('%d-%m-%Y')

                message_bunkers = ''
                bunkerstotal = session.query(func.count(Flights.flights), Flights.last_name, Flights.date, Flights.user_id).group_by(Flights.last_name).all()
                for item in bunkerstotal:
                    if item[3] != '199196080':
                        message_bunkers += f'{item[1]} - {item[0]}\n'

                message_tonnes = ''
                tonnestotal = session.query(func.sum(Tonnes.tonnes), Tonnes.user_id).group_by(Tonnes.user_id)
                for item in tonnestotal:
                    if item[1] != '199196080':
                        message_tonnes += str(item[0])

                message_kilometers = ''
                kilometerstotal = session.query(func.sum(Kilometers.kilometers), Kilometers.user_id).group_by(Kilometers.user_id)
                for item in kilometerstotal:
                    if item[1] != '199196080':
                        message_kilometers += str(item[0])

                message_flights = ''
                flightstotal = session.query(func.sum(Flights.flights), Flights.user_id).group_by(Flights.user_id)
                for item in flightstotal:
                    if item[1] != '199196080':
                        message_flights += str(item[0])

                sender(user_id, f'Общая статистика:\nБункеры:\n{message_bunkers}\n{message_tonnes} тонн.\n{message_kilometers} километров.\n{message_flights} рейсов.')

            if msg == 'статистика':
                tonnestotal = session.query(func.sum(Tonnes.tonnes)).filter(Tonnes.user_id == user_id)[0][0]
                kilometerstotal = session.query(func.sum(Kilometers.kilometers)).filter(Kilometers.user_id == user_id)[0][0]
                flightsindaytotal = session.query(func.sum(Flightsinday.flightsinday)).filter(Flightsinday.user_id == user_id)[0][0]
                # flightstotal = session.query(func.count(Flights.flights)).filter(Flights.user_id == user_id)[0][0]
                sender(user_id, f'За всё время:\n{round(tonnestotal, 2)} тонн.\n{kilometerstotal} километров.\n{flightsindaytotal} рейсов')

            if msg == 'формула':
                sender(user_id, '0.01 * (33.5 * общий пробег + 1.3 * на расстояние * на тонны) * (1 + 0.01 * 40) + (0.5 * количество рейсов)')

            if msg == 'клавиатура':
                keyboard = VkKeyboard()
                keyboard.add_button('Завершить рейс')
                keyboard.add_line()
                keyboard.add_button('Тонны за сегодня')
                keyboard.add_button('Рейсы за сегодня')
                keyboard.add_line()
                keyboard.add_button('Бункеры за сегодня')
                keyboard.add_button('Бункеры за вчера')
                keyboard.add_line()
                keyboard.add_button('Формула')
                keyboard.add_line()
                keyboard.add_button('Статистика')

                sender(user_id, 'ОК!', keyboard)

            qwerty(msg_update)

if __name__ == '__main__':
    flight()