from flask import Flask, render_template, request
import datetime
import json

app = Flask(__name__)

now = datetime.datetime.now()
today_date = now.strftime('%H:%M')

DB_FILE = './data/db.json'
db = open(DB_FILE, 'rb')
data = json.load(db)
messages = data['messages']

def save_messages_to_file():
    db = open(DB_FILE, 'w')
    data = {
        'messages': messages
    }
    json.dump(data, db)

def add_message(text, sender): #объявим функцию, которая добавит соообщение в список
    new_message = {
        "text": text,
        "sender": sender,
        "time": today_date #toDO: указать правильное время/дату
    }
    messages.append(new_message) #Добавляем новое сообщение в список
    save_messages_to_file()

def print_message(message): #объявляем функцию, которая будет печатать одно сообщение
    print(f"[{message['sender']}]: {message['text']} --- {message['time']}")

for message in messages:
    print_message(message)

# Главная страница
@app.route('/')
def index_page():
    return 'Здравствуйте, вас приветствует SkillChat'

@app.route('/get_messages')
def get_messages():
    return { 'messages': messages }

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/send_message')
def send_message():
    name = request.args['name']
    text = request.args['text']

    add_message(text, name)
    return 'OK'

app.run()