from db import People, session
import datetime
from sqlalchemy import func

msg = input('Должность: ')

query = session.query(People).order_by(People.rang.desc()).all()
# print(query)
q = ''

for i in query:
    q += (f'{i.nickname} {[i.rang]} {i.post}\n')

print(q)

# if session.query(People).filter(People.nickname == msg):
#     print('Есть')
# else:
#     print('Неесть')