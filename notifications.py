from notifiers import get_notifier
import time
from TOKEN import token
import telebot
bot = telebot.TeleBot(token)


class Sender:
    nameOfNoti = None #имя заметки
    time = None #время до отправки
    content = None #содержание
    date = None #дата отправки

    def __init__(self):
        self.nameOfNoti = ""
        self.time = ""
        self.content = ""
        self.date = ""

    def setName(self,message):
        self.nameOfNoti = message.text
        bot.send_message(message.chat.id,'Имя задано: ' + message.text)

    def setContent(self, message):
        bot.send_message(message.chat.id, 'Введите содержимое для заметки:\n')
        self.content = message.text
        bot.send_message(message.chat.id,'Содержимое: ' + message.text)

    def setDate(self, message):
        bot.send_message(message.chat.id, 'Введите дату для заметки:\n')
        self.content = message.text
        bot.send_message(message.chat.id,'Дата задана: ' + message.text)

    def setTime(self, message):
        bot.send_message(message.chat.id, 'Введите время для заметки:\n')
        self.time = message.text
        bot.send_message(message.chat.id, 'Время для заметки: ' + message.text)


    def getInfo(self,chatId):
        bot.send_message(chatId, "Имя заметки: " + self.nameOfNoti + "\nВремя отправки: " + self.time + "\nДата отправки: " + self.date + "\nСодержание: " + self.content)


    def sendNoti(self) :
        t = int(self.time) * 60 #задержка перед отправкой в минутах
        time.sleep(t)
        telegram = get_notifier('telegram') #название переменной для использования методов отправки уведомлений
        telegram.notify(token=token, chat_id=chatId, message=self.nameOfNoti)

    @bot.message_handler(commands=['fhjd'])
    def botSetName (self,message):
            bot.register_next_step_handler(message,self.setName)

    def botSetContent (self,message):
            bot.register_next_step_handler(message,self.setContent)

    def botSetTime (self,message):
            bot.register_next_step_handler(message,self.setTime)

    def botSetDate (self,message):
            bot.register_next_step_handler(message,self.setDate)

