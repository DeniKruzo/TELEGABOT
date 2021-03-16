import telebot
import sqlite3


#Если считать с файла выдаст - Error code: 404. Description: Not Found
#file = open('botKey.txt', 'r')
#TOKEN = file.read()
#print(str(TOKEN))
#bot = telebot.TeleBot(str(TOKEN))

try:
    conn = sqlite3.connect("DatBas.sqlite", check_same_thread=False)
    cursor = conn.cursor()
except:
    print("ой...ошибка!")

try:
    querry = '''CREATE TABLE table1 (id INTEGER, word TEXT NOT NULL)'''
    cursor.execute(querry)
    conn.commit()
    cursor.close()
except sqlite3.OperationalError:
    pass

bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Я бот! \nСписок команд: /reply \n(переслать ваше последнее сообщение) \n /myid \n(узнать ваш id)")


@bot.message_handler(commands=['myid'])
def send_reply(message):
    bot.reply_to(message, message.from_user.id)


@bot.message_handler(commands=['reply'])
def send_reply(message):
    people_id = message.from_user.id
    cursor = conn.cursor()
    cursor.execute('''SELECT word FROM table1 WHERE id= (?)''', (people_id, ))
    record1 = cursor
    bot.reply_to(message, record1)
    cursor.close()
    print(record1)

@bot.message_handler(content_types=['text'])
def welcome(message):
    people_id = message.from_user.id
    if message.text != "/reply":

        if message.from_user.last_name == None:
            bot.send_message(message.from_user.id, "Привет, " + message.from_user.first_name)
        else:
            bot.send_message(message.from_user.id,
                             "Привет, " + message.from_user.first_name + message.from_user.last_name)
        record = message.text
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO table1 (id, word) VALUES (?, ?)''', (people_id, record, ))
        cursor.execute('''UPDATE table1 SET word = ? WHERE id = ?''', (record, people_id,))
        conn.commit()
        cursor.close()


#file.close()
bot.polling(none_stop=True)