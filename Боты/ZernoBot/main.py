from db import Order, Active_Order, Settings, session
import datetime
from sqlalchemy import func

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import re

vk_session = vk_api.VkApi(token = 'bc17c5430daf4e0ebd9817dc009091e616ce96fa32447d704b5eab77af6bbb58c1c21a588d61c3cf6dccd')
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

def add_order():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id
            msgup = msg.split()

            now = datetime.datetime.now()
            today_date = now.strftime('%d-%m-%Y')

            user_id = user_id
            tonnes = float(msgup[0])
            price = session.query(Settings).filter(Settings.user_id == user_id).first().price
            people = msgup[1]
            total_cash = float(tonnes) * float(price)
            your_cash = float(total_cash) / float(people)

            # user_id = user_id
            # tonnes = float(msg)
            # print(type(tonnes))
            # price = session.query(Settings).filter(Settings.user_id == user_id).first().price
            # people = session.query(Settings).filter(Settings.user_id == user_id).first().people
            # total_cash = float(tonnes) * float(price)
            # your_cash = float(total_cash) / float(people)

            act_order = Active_Order(user_id=user_id, tonnes=tonnes, people=people, total_cash=total_cash, your_cash=your_cash, date=today_date)
            session.add(act_order)
            session.commit()

            sender(user_id, 'Заказ ожидает выполнения🕓.\nВсе активные заказы можно посмотреть в разделе "Активные заказы🕓"')

            active_orders()

            return main()

def profit():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            msg = event.text.lower()
            msgup = msg.split()
            tonnes = float(msgup[0])
            price = session.query(Settings).filter(Settings.user_id == user_id).first().price
            people = msgup[1]

            profit_total = round(tonnes * int(price))
            profit_your = round(profit_total / float(people))

            sender(user_id, f'{msgup[0]} тонн🌾\n{msgup[1]} человека👥\n\nКаждый заработает по {str(profit_your)}₽💸\nВсего вы заработаете {str(profit_total)}₽💸')

            return main()

def active_orders():
    for event in longpoll.listen():
        user_id = event.user_id

        for i in range(len(session.query(Active_Order).filter(Active_Order.user_id == user_id).all())):
            query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[i]

            user_id = query_data.user_id
            tonnes = query_data.tonnes
            people = query_data.people
            total_cash = query_data.total_cash
            your_cash = query_data.your_cash

            keyboard = VkKeyboard(inline=True)
            keyboard.add_button('Завершить(' + str(i + 1) +')', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Отменить(' + str(i + 1) +')', color=VkKeyboardColor.NEGATIVE)

            sender(user_id,  '╭═─═──═──═─≪⌘≫─═──═──═──═╮\n' + '⠀⠀⠀⠀⠀⠀⠀Активный заказ🕓:\n\n' + '⠀⠀⠀⠀⠀⠀⠀⠀⠀' + str(tonnes) + ' тонн🌾\n' + '⠀⠀⠀⠀⠀⠀⠀⠀' + str(people) + ' человека👥\n' + '⠀⠀⠀⠀⠀⠀⠀' + str(round(your_cash)) + '₽ прибыль💸\n' + '⠀⠀⠀⠀⠀' + str(round(total_cash)) + '₽ прибыль всего💸\n', keyboard)

        return main()

def change_settings():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id

            # Обработчик смайлов
            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
            msg = emoji_pattern.sub(r'', msg)

            if msg == 'цена за тонну':
                current_total_cash = session.query(Settings).filter(Settings.user_id == user_id).first().price

                sender(user_id, 'Текущее значение: ' + str(current_total_cash))
                sender(user_id, 'Установите новое значение:')

                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        keyboard = VkKeyboard()
                        keyboard.add_button('Заказ📞')
                        keyboard.add_line()
                        keyboard.add_button('Всего📑')
                        keyboard.add_line()
                        keyboard.add_button('Прибыль💸')
                        keyboard.add_line()
                        keyboard.add_button('Настройки🛠')

                        prices = event.text.lower()
                        user_id = event.user_id

                        settings_price = session.query(Settings).filter(Settings.user_id == user_id).first()
                        settings_price.price = prices

                        sender(user_id, 'Данные сохранены✔', keyboard)
                        return main()

            # if msg == 'кол-во человек':
            #     current_total_cash = session.query(Settings).filter(Settings.user_id == user_id).first().people

            #     sender(user_id, 'Текущее значение: ' + str(current_total_cash))
            #     sender(user_id, 'Установите новое значение:')

            #     for event in longpoll.listen():
            #         if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            #             peoples = event.text.lower()
            #             user_id = event.user_id

            #             settings_people = session.query(Settings).filter(Settings.user_id == user_id).first()
            #             settings_people.people = peoples

            #             sender(user_id, 'Данные сохранены✔')
            #             break

            # if msg == 'главное меню':
            #     keyboard = VkKeyboard()
            #     keyboard.add_button('Заказ📞')
            #     keyboard.add_button('Всего📑')
            #     keyboard.add_button('Прибыль💸')
            #     keyboard.add_line()
            #     keyboard.add_button('Настройки🛠')

            #     sender(user_id, 'Удачи!🍃',keyboard)
            #     return main()

def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id

            # Обработчик смайлов
            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
            msg = emoji_pattern.sub(r'', msg)

            if msg == 'начать':
                keyboard = VkKeyboard()
                keyboard.add_button('Заказ📞')
                keyboard.add_line()
                keyboard.add_button('Всего📑')
                keyboard.add_line()
                keyboard.add_button('Прибыль💸')
                keyboard.add_line()
                keyboard.add_button('Настройки🛠')

                keyboard_two = VkKeyboard(inline=True)
                keyboard_two.add_button('Настроить', color=VkKeyboardColor.PRIMARY)

                sender(user_id, 'Есть десептиконы...есть автоботы...а есть зерноботы😹\n\n' +
                    '⚠📜Инструкция пользования:\n\n' +
                    '📞С помощью кнопки "Заказ" можно добавить заказ. Данные о заказе будут сохранены и доступны для просмотра в статистике.\n\n' +
                    '📑Кнопка "Всего" выведет подробную статистику.\n\n' +
                    '🛠Перед началом использования, нужно добавить необходимые настройки. Этап настройки является обязательным перед началом пользования. После первичной настройки, настройки можно менять по мере необходимости.\n\n' +
                    '💸Кнопка "Прибыль" запускает калькулятор возможной прибыли, без сохранения данных.\n\n' +
                    'При добавлении заказа боту нужно знать только количество тонн, остальные данные(цену за тонну и кол-во человек, выполняющих заказ)он берёт из настроек, которые вы сохранили.\n' +
                    'Соответственно, в случае, если будут изменения в цене или количестве людей, сначала нужно будет внести поправки в настройки, а затем создавать заказ.\n' +
                    'После добавления заказа - заказ считается активным и данные о нём не отображаются в статистике. Для отображения в статистике, заказ нужно завершить.\n\n' +
                    '🖊✉По всем вопросам:\nhttps://vk.com/r_alexandrovich', keyboard)

                sender(user_id, 'Если вопросов не осталось, предлагаю перейти к настройкам. В настройках указывается цена за тонну и количество человек, выполняющих заказ', keyboard_two)

            if msg == 'настроить':
                keyboard = VkKeyboard()
                keyboard.add_button('Цена за тонну💸')
                # keyboard.add_button('Кол-во человек👥')
                # keyboard.add_line()
                # keyboard.add_button('Главное меню🔙')

                settings = Settings(user_id=user_id, price=0)
                session.add(settings)
                session.commit()

                sender(user_id, 'Выберите категорию:', keyboard)

                change_settings()

            if msg == 'настройки':
                keyboard = VkKeyboard()
                keyboard.add_button('Цена за тонну💸')
                # keyboard.add_button('Кол-во человек👥')
                # keyboard.add_line()
                # keyboard.add_button('Главное меню🔙')

                sender(user_id, 'Выберите категорию:', keyboard)

                change_settings()

            if msg == 'заказ':
                sender(user_id, 'На сколько тонн?🌾')

                add_order()
                
            if msg == 'всего':
                now = datetime.datetime.now()
                today_date = now.strftime('%d-%m-%Y')

                # Данные за день и за всё время.
                orders_count_total = session.query(func.count(Order.order_id)).filter(Order.user_id == user_id).all()[-1]
                orders_count_day = session.query(func.count(Order.order_id)).filter(Order.user_id == user_id).filter(Order.date == today_date).all()[-1]
                statistics_total = session.query(func.sum(Order.tonnes), func.sum(Order.total_cash), func.sum(Order.your_cash)).filter(Order.user_id == user_id).all()
                for statistics_total in statistics_total:
                    pass
                statistics_day = session.query(func.sum(Order.tonnes), func.sum(Order.total_cash), func.sum(Order.your_cash)).filter(Order.user_id == user_id).filter(Order.date == today_date)
                for statistics_day in statistics_day:
                    pass

                # Самый тяжёлый заказ
                order_hard_total = session.query(Order.date, func.max(Order.tonnes), Order.people, Order.total_cash, Order.your_cash).filter(Order.user_id == user_id).all()
                for order_hard_total in order_hard_total:
                    pass

                # Самый тяжёлый день
                day_hard_total = session.query(Order.date, func.sum(Order.tonnes), func.count(Order.date), func.sum(Order.total_cash), func.sum(Order.your_cash)).group_by(Order.date).filter(Order.user_id == user_id).all()
                def custom_key(tonnes):
                    return tonnes[1]
                day_hard_total.sort(key=custom_key)

                sender(user_id, '╭═──═──═──≪⌘≫──═──═──═╮\n'
                    + '⠀⠀⠀⠀⠀⠀⠀—За сегодня—\n' + str(orders_count_day[-1]) + ' заказов' + '⠀' + str(statistics_day[0]) + ' тонн🌾' + '⠀' + str(statistics_day[1]) + '₽💸\n\n' + '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀' + str(statistics_day[2]) + '₽💸\n\n' + '⠀⠀⠀⠀⠀⠀—За всё время—\n' + str(orders_count_total[-1]) + ' заказов' + '⠀' + str(statistics_total[0]) + ' тонн🌾' + '⠀' + str(statistics_total[1]) + '₽💸\n\n' + '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀' + str(statistics_total[2]) + '₽💸\n' +
                    '╰═──═──═──≪⌘≫──═──═──═╯\n\n'
                    + '४॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰४\n\n' +
                    '╭═──═──═──≪⌘≫──═──═──═╮\n'
                    + '⠀⠀⠀—Самый трудный заказ—\n\n' + '⠀⠀⠀⠀—Заказ от ' + str(order_hard_total[0]) + '—\n\n' + '⠀⠀⠀⠀⠀⠀⠀⠀' + str(order_hard_total[1]) + ' тонн🌾\n' + '⠀⠀⠀⠀⠀⠀⠀' + str(order_hard_total[2]) + ' человека👥\n' + '⠀⠀⠀⠀⠀' + str(order_hard_total[4]) + '₽ прибыль💸\n' + '⠀⠀⠀' + str(order_hard_total[3]) + '₽ прибыль(всего)💸\n' +
                    '╰═──═──═──≪⌘≫──═──═──═╯\n\n'
                    + '४॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰॰४\n\n' +
                    '╭═──═──═──≪⌘≫──═──═──═╮\n'
                    + '⠀⠀⠀—Самый трудный день—\n\n' + '⠀⠀⠀⠀⠀⠀⠀—' + str(day_hard_total[-1][0]) + '—\n\n' + '⠀⠀⠀⠀⠀⠀⠀⠀' + str(day_hard_total[-1][2]) + ' заказов\n' + str(day_hard_total[-1][1]) + ' тонн🌾⠀⠀⠀⠀⠀⠀⠀⠀⠀' + str(day_hard_total[-1][3]) + '₽💸\n\n' + '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀' + str(day_hard_total[-1][4]) + '₽💸' +
                    '╰═──═──═──≪⌘≫──═──═──═╯')

            if msg == 'прибыль':
                sender(user_id, 'Сколько тонн?🌾')

                profit()
            
            if msg == 'завершить(1)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[0]
    
                user_id = query_data.user_id
                tonnes = query_data.tonnes
                people = query_data.people
                total_cash = query_data.total_cash
                your_cash = query_data.your_cash
                date = query_data.date

                orders = Order(user_id=user_id, tonnes=tonnes, people=people, total_cash=total_cash, your_cash=your_cash, date=date)
                session.add(orders)
                session.commit()
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ завершён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'завершить(2)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[1]

                user_id = query_data.user_id
                tonnes = query_data.tonnes
                people = query_data.people
                total_cash = query_data.total_cash
                your_cash = query_data.your_cash
                date = query_data.date

                orders = Order(user_id=user_id, tonnes=tonnes, people=people, total_cash=total_cash, your_cash=your_cash, date=date)
                session.add(orders)
                session.commit()
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ завершён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'завершить(3)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[2]

                user_id = query_data.user_id
                tonnes = query_data.tonnes
                people = query_data.people
                total_cash = query_data.total_cash
                your_cash = query_data.your_cash
                date = query_data.date

                orders = Order(user_id=user_id, tonnes=tonnes, people=people, total_cash=total_cash, your_cash=your_cash, date=date)
                session.add(orders)
                session.commit()
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ завершён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'завершить(4)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[3]

                user_id = query_data.user_id
                tonnes = query_data.tonnes
                people = query_data.people
                total_cash = query_data.total_cash
                your_cash = query_data.your_cash
                date = query_data.date

                orders = Order(user_id=user_id, tonnes=tonnes, people=people, total_cash=total_cash, your_cash=your_cash, date=date)
                session.add(orders)
                session.commit()
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ завершён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'завершить(5)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[4]

                user_id = query_data.user_id
                tonnes = query_data.tonnes
                people = query_data.people
                total_cash = query_data.total_cash
                your_cash = query_data.your_cash
                date = query_data.date

                orders = Order(user_id=user_id, tonnes=tonnes, people=people, total_cash=total_cash, your_cash=your_cash, date=date)
                session.add(orders)
                session.commit()
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ завершён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'завершить(6)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[5]

                user_id = query_data.user_id
                tonnes = query_data.tonnes
                people = query_data.people
                total_cash = query_data.total_cash
                your_cash = query_data.your_cash
                date = query_data.date

                orders = Order(user_id=user_id, tonnes=tonnes, people=people, total_cash=total_cash, your_cash=your_cash, date=date)
                session.add(orders)
                session.commit()
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ завершён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'активные заказы':
                order_count = session.query(func.count(Active_Order.order_id))[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'отменить(1)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[0]
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ отменён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'отменить(2)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[1]
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ отменён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'отменить(3)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[2]
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ отменён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'отменить(4)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[3]
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ отменён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'отменить(5)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[4]
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ отменён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

            if msg == 'отменить(6)':
                query_data = session.query(Active_Order).filter(Active_Order.user_id == user_id).all()[5]
                session.delete(query_data)
                session.commit()

                sender(user_id, 'Заказ отменён!✅\nЧтобы узнать сколько вы занесли нажмите кнопку "Всего📑"')

                order_count = session.query(func.count(Active_Order.order_id)).filter(Active_Order.user_id == user_id)[-1][-1]
                if order_count != 0:
                    active_orders()
                else:
                    sender(user_id, 'Активных заказов нет!😌\nКажется, можно отдохнуть.🍃')

if __name__ == '__main__':
    main()