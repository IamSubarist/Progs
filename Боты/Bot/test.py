# from db import *

# # message = ''
# # name = session.query(Flight.last_name)

# # for item in name:
# #     num = session.query(Flight.last_name, func.count(Flight.flight_number)).filter(Flight.last_name == item[0])
# #     print(num[0])
# #     message += f'{num[0][0]} '

# # message1 = message.split()
# # message2 = list(set(message1))

# # m = ''
# # for i in message2:
# #     query = session.query(func.count(Flight.flight_number)).filter(Flight.last_name == i)
# #     # print(f'{i} x {query[0][0]}')
# #     m += f'{i} x {query[0][0]}__'
# # print(m)
# last_names = {
#             'Мелащенко': 'милащенко мелащинко мелащенко',
#             'Яценко': 'яцун яценко',
#             'Осадчий': 'осачий осадчий асачий асадчий',
#             'Редкоус': 'федорович фёдорович редкаус редкоус ридкаус ридкоус',
#             'Бабичев': 'бабич бабичев',
#             'Мухтаров': 'шамиль шомиль муха мухтаров',
#         }

# a = input('Введите текст: ')
# c = []
# c = a.split()
# def qwerty(arg):
#     if len(arg) == 2:
#         for key, value in last_names.items():
#             value = value.split()
#             for i in value:
#                 if arg[0] == i and not arg[1]:
#                     flight = Flight(flight_number=1, user_id='123', last_name=key)
#                     session.add(flight)
#                     session.commit()

#                     print('ОК!')
#                     print(f'{arg[0]} {arg[1]}')
#         if arg[1] == 'последний':
#             # total = session.query(Flight)
#             last_name = session.query(Flight.last_name)
#             message = ''

#             for item in last_name:
#                 num = session.query(Flight.last_name, func.count(Flight.flight_number)).filter(Flight.last_name == item[0])
#                 message += f'{num[0][0]} '

#             split = message.split()
#             sets = list(set(split))

#             messages = ''
#             for item in sets:
#                 query = session.query(func.count(Flight.flight_number)).filter(Flight.last_name == item)
#                 messages += f'{item} x {query[0][0]}\n'

#                 print(messages)

#             # for item in total:
#             #     session.delete(item)
#             #     session.commit()
#         else:
#             print('Возможно в предложении есть ошибка!')
#     else:
#         for key, value in last_names.items():
#             value = value.split()
#             for i in value:
#                 if arg[0] == i:
#                     flight = Flight(flight_number=1, user_id='123', last_name=key)
#                     session.add(flight)
#                     session.commit()

#                     print('ОК!')
#                     print(f'{arg[0]}')
# qwerty(c)

#     # for key, value in last_names.items():
#     #     value = value.split()
#     #     for i in value:
#     #         if arg[0] == i:
#     #             flight = Flight(flight_number=1, user_id='123', last_name=key)
#     #             session.add(flight)
#     #             session.commit()

#     #             print('ОК!')

#     #         if arg[1] == 'последний':
#     #             total = session.query(Flight)
#     #             last_name = session.query(Flight.last_name)
#     #             message = ''

#     #             for item in last_name:
#     #                 num = session.query(Flight.last_name, func.count(Flight.flight_number)).filter(Flight.last_name == item[0])
#     #                 message += f'{num[0][0]} '

#     #             split = message.split()
#     #             sets = list(set(split))

#     #             messages = ''
#     #             for item in sets:
#     #                 query = session.query(func.count(Flight.flight_number)).filter(Flight.last_name == item)
#     #                 messages += f'{item} x {query[0][0]}\n'

#     #                 print(messages)

#     #             for item in total:
#     #                 session.delete(item)
#     #                 session.commit()

# import re

# name = input('Введите: ')
# nameup = re.split('[ : /]', name)
# print(name)
# print(nameup).
import datetime
from datetime import date, timedelta

now = datetime.datetime.now()

today_date = now.strftime('%d-%m-%Y')

today_dateday = int(now.strftime('%d'))
today_date2 = now.strftime('-%m-%Y')

fin = f''
# print(today_dateday - 1)
# print(f'{tdup_day - 1}{today_date2}')

print(today_date)
print(date.today())
print(date.today() - timedelta(days=1))