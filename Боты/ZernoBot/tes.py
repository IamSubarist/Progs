from sqlalchemy import func
from db import Order, Active_Order, Settings, session
import datetime
import re

# prices = input('Введи: ')
# query = session.query(Settings).first()
# query.price = prices

# order_count = session.query(func.count(Active_Order.order_id))[-1][-1]
# if order_count == 0:
#     print('Активных заказов больше нет! Кажется, можно отдохнуть.')
# else:
#     print('dfjkvkljfsgskdvhsjkdfhsdfhvdf')

# text = u'This dog \U0001f602'
# print(text) # with emoji

# emoji_pattern = re.compile("["
#     u"\U0001F600-\U0001F64F"  # emoticons
#     u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#     u"\U0001F680-\U0001F6FF"  # transport & map symbols
#     u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                        "]+", flags=re.UNICODE)
# print(emoji_pattern.sub(r'', text)) # no emoji


# now = datetime.datetime.now()
# today_date = now.strftime('%d-%m-%Y')

# .filter(Order.user_id == user_id)

# query_day_orders = session.query(func.count(Order.order_id)).filter(Order.date == today_date).all()
# print(query_day_orders[-1])


# query_days = session.query(func.sum(Order.tonnes), func.sum(Order.value), func.sum(Order.summ)).filter(Order.date == today_date).filter(Order.user_id == )
# for query_day in query_days:
#     pass

# print(query_day[0])

# print(session.query(Order.user_id).first())





# query_hard_order = session.query(Order.date, func.max(Order.tonnes), Order.people, Order.value, Order.summ).all()
# for query_hard_order in query_hard_order:
#     print(query_hard_order)



# query_date = session.query(Order.date, func.sum(Order.tonnes), func.count(Order.date), func.sum(Order.value), func.sum(Order.summ)).group_by(Order.date).all()
# # print(query_date)

# def custom_key(tonnes):
#     return tonnes[1]

# query_date.sort(key=custom_key)
# print(query_date[-1])




# now = datetime.datetime.now()
# today_date = now.strftime('%d-%m-%Y')

# query_total = session.query(func.sum(Order.tonnes), func.sum(Order.value), func.sum(Order.summ)).all()

# for query_totals in query_total:
#     print(query_totals[0])
#     print(query_totals[1])
#     print(query_totals[2])

# query_day = session.query(func.sum(Order.tonnes), func.sum(Order.value), func.sum(Order.summ)).filter(Order.date == today_date).all()

# for query_days in query_day:
#     pass
    # print(query_days)

# query_orders_total = session.query(Order.order_id).all()
# query_orders_day = session.query(Order.order_id).filter(Order.date == today_date).all()

# query_tonnes_total = session.query(func.sum(Order.tonnes))
# query_tonnes_day = session.query(func.sum(Order.tonnes).filter(Order.date == today_date))

# query_profit_total = session.query(func.sum(Order.value))
# query_profit_day = session.query(func.sum(Order.value).filter(Order.date == today_date))

# query_summ_total = session.query(func.sum(Order.summ))
# query_summ_day = session.query(func.sum(Order.summ).filter(Order.date == today_date))

# print(query_orders_total[-1][-1])
# print(query_orders_day[-1][-1])

# for tonnes_total in query_tonnes_total:
#     for tonnes_day in query_tonnes_day:
#         print(tonnes_total[-1])
#         print(tonnes_day[-1])

# for profit_total in query_profit_total:
#     for profit_day in query_profit_day:
#         print(profit_total[-1])
#         print(profit_day[-1])

# for summ_total in query_summ_total:
#     for summ_day in query_summ_day:
#         print(summ_total[-1])
#         print(summ_day[-1])