import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Order

engine = create_engine('sqlite:///zernoapp.sqlite', echo=True)
Session = sessionmaker(bind=engine)
s = Session()

now = datetime.datetime.now()
today_date = now.strftime('%d-%m-%Y')

tonnes = int(input('Тонны:'))
culture = input('Что кидаете:')
people = int(input('Сколько вас:'))
value = tonnes * 450
summ = value / people

order_one = Order(tonnes=tonnes, culture=culture, people=people, value=value, summ=summ, date=today_date)
s.add(order_one)
s.commit()

# order_two = Order(tonnes=15, culture='wheat', people=2, value=900, summ=450, date=today_date)
# s.add(order_two)
# s.commit()