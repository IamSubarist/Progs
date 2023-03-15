from db import People, session
import datetime
from sqlalchemy import func
import threading

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import re

def thread_function():
    while True:
        try:
            vk.messages.setActivity(group_id=-217771495,type='typing',peer_id=2000000000 + 1)
            time.sleep(150) #150 это задержка, если код много жрёт поставьте больше
        except:
            pass
if __name__ == "__main__":
    x1 = threading.Thread(target=thread_function, args=())
    x1.start()

while True:
    vk_session = vk_api.VkApi(token = 'vk1.a.H215x8ULC-KoLe8eCJ0FEfNvZ0OsFpLdaWyTufYiKC4Y9IQWGCqOZGz3QkPzb18QLEC0bTteQUXZfPIn6_jfTbxV_gcRzi9wVefIutc_WeDafoooc7YdV1AR7JymzWYSo4ehLYl0RRjhChuEclYRj53XBVdE2mGxs0FhM-Nv5fiksrqje0ccZajca_geo4RQ48OIWeKpGjNmSKciBpD5Hg')
    session_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    print('Бот запущен.')
    try:
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

        def add_people():
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text
                    user_id = event.user_id

                    msg_up = msg.split(' ')

                    if len(msg_up) > 1:
                        name = msg_up[0]
                        rang = msg_up[1]

                        rang_post = {
                            '1': 'Водитель',
                            '2': 'Охранник',
                            '3': 'Начальник Охраны',
                            '4': 'Секретарь',
                            '5': 'Старший Секретарь',
                            '6': 'Лицензёр',
                            '7': 'Адвокат',
                            '8': 'Депутат',
                            '9': 'Вице-губернатор',
                            '10': 'Губернатор',
                        }

                        for key, value in rang_post.items():
                            if rang == key:

                                nickname = name
                                rang = key
                                post = value

                                new_people = People(user_id=user_id, nickname=name, rang=rang, post=post, raising='Не повышался')
                                session.add(new_people)
                                session.commit()

                                sender(user_id, f'Сотрудник {name} добавлен в базу. Должность: {value}.')
                                return main()
                    else:
                        sender(user_id, 'Информация введена неправильно, попробуйте снова!\nПодсказка: Имя_Фамилия Ранг')

        def dismiss_people():
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text
                    user_id = event.user_id
                    
                    find_people = session.query(People).filter(People.nickname == msg)[0]

                    session.delete(find_people)
                    session.commit()

                    sender(user_id, f'Сотрудник {find_people.nickname} [{find_people.rang}] {find_people.post} удалён.')
                    return main()

        def check_people():
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text
                    user_id = event.user_id

                    query = session.query(People.nickname).filter(People.user_id == user_id).all()

                    for i in query:

                        if msg == i[0]:

                            find_people = session.query(People).filter(People.nickname == msg)[0]

                            if find_people.raising == 'Не повышался':
                                sender(user_id, f'Сотрудник {find_people.nickname} [{find_people.rang}] {find_people.post}. Сегодня НЕ повышался.')
                            else:
                                sender(user_id, f'Сотрудник {find_people.nickname} [{find_people.rang}] {find_people.post}. Уже повышался сегодня.')
                            
                            return main()
                    # else:
                    #     sender(user_id, 'Такого сотрудника нет.\nВозможно вы допустили ошибку, проверьте правильность ввода.')

        def up_people():
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text
                    user_id = event.user_id  
                    msg_up = msg.split(' ')
                    
                    if len(msg_up) > 1:
                        name = msg_up[0]
                        rang = msg_up[1]

                        rang_post = {
                            '1': 'Водитель',
                            '2': 'Охранник',
                            '3': 'Начальник Охраны',
                            '4': 'Секретарь',
                            '5': 'Старший Секретарь',
                            '6': 'Лицензёр',
                            '7': 'Адвокат',
                            '8': 'Депутат',
                            '9': 'Вице-губернатор',
                            '10': 'Губернатор',
                        }

                        find_peoples = session.query(People).filter(People.user_id == user_id).filter(People.nickname == name)[0]
                        session.delete(find_peoples)
                        session.commit()

                        for key, value in rang_post.items():
                            if rang == key:

                                nickname = name
                                rang = key
                                post = value

                                up_peoples = People(user_id=user_id, nickname=name, rang=rang, post=post, raising='Повышен')
                                session.add(up_peoples)
                                session.commit()

                                sender(user_id, f'Данные о сотруднике обновлены, сотрудник повышен: {name} [{rang}] {post}')
                                return main()
                    else:
                        sender(user_id, 'Информация введена не по форме, попробуйте снова!\nПодсказка: Имя_Фамилия Ранг')

        # def reload_raising():
        #     find_peoples = session.query(People).filter(People.user_id == user_id).all()
        #     for i in find_peoples:
        #         i.raising = 'Не повышался'
        #         session.commit()
            
        #     sender(user_id, 'Повышения сброшены!')
        #     return main()

        def find_post():
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text
                    user_id = event.user_id 

                    post_peoples = ''
                    
                    find_post_peoples = session.query(People).filter(People.user_id == user_id).filter(People.post == msg).all()
                    for i in find_post_peoples:
                        post_peoples += (f'\n{i.nickname} {i.rang} {i.post}')

                    count_peoples = session.query(People).filter(People.post == msg).count()
                    sender(user_id, f'В Правительстве {count_peoples} сотрудников с должностью: {msg}\n{post_peoples}.')

                    return main()

        # def all_people():
        #     all_peoples = ''
                    
        #     find_all_peoples = session.query(People).all()
        #     for i in find_all_peoples:
        #         all_peoples += (f'\n{i.nickname} {i.rang} {i.post}')

        #     count_peoples = session.query(People).count()
        #     sender(user_id, f'В Правительстве {count_peoples} сотрудников.\n{all_peoples}')

        #     return main()

        def main():
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text.lower()
                    user_id = event.user_id

                    if msg == 'начать':
                        keyboard = VkKeyboard()
                        keyboard.add_button('Добавить сотрудника', color=VkKeyboardColor.POSITIVE)
                        keyboard.add_button('Удалить сотрудника', color=VkKeyboardColor.NEGATIVE)
                        keyboard.add_line()
                        keyboard.add_button('Проверить сотрудника')
                        keyboard.add_button('Повысить сотрудника', color=VkKeyboardColor.POSITIVE)
                        keyboard.add_line()
                        keyboard.add_button('Сброс повышений')
                        keyboard.add_line()
                        keyboard.add_button('Просмотр сотрудников по должности')
                        keyboard.add_line()
                        keyboard.add_button('Все сотрудники')
                        
                        sender(user_id, 'Вы начали работу с ботом.', keyboard)

                    if msg == 'добавить сотрудника':
                        sender(user_id, 'Имя_Фамилия Ранг')
                        add_people()
                    
                    if msg == 'удалить сотрудника':
                        sender(user_id, 'Имя_Фамилия')
                        dismiss_people()
                    
                    if msg == 'проверить сотрудника':
                        sender(user_id, 'Имя_Фамилия')

                        check_people()

                    if msg == 'повысить сотрудника':
                        sender(user_id, 'Имя_Фамилия Ранг')

                        up_people()
                    
                    if msg == 'сброс повышений':
                        find_peoples = session.query(People).filter(People.user_id == user_id).all()
                        for i in find_peoples:
                            i.raising = 'Не повышался'
                            session.commit()
                        sender(user_id, 'Сегодняшние повышения сброшены!')

                    if msg == 'все сотрудники':
                        all_peoples = ''
                    
                        find_all_peoples = session.query(People).filter(People.user_id == user_id).order_by(People.rang.desc()).all()
                        
                        for i in find_all_peoples:
                            all_peoples += (f'\n{i.nickname} {i.rang} {i.post}')

                        count_peoples = session.query(People).count()
                        sender(user_id, f'В Правительстве {count_peoples} сотрудников.\n{all_peoples}')

                    if msg == 'просмотр сотрудников по должности':
                        sender(user_id, 'НазваниеДолжности')
                        
                        find_post()

        if __name__ == '__main__':
            main()
    except Exception:
        pass

