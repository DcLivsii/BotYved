from notifications import bot, Sender
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

example = Sender()
array = []
waiting_for_message_reply = set()


@bot.message_handler(commands=['start'])
def start(message):
     markup = ReplyKeyboardMarkup(resize_keyboard = True)
     item1 = KeyboardButton('💌 Список задач')
     item2 = KeyboardButton('💬 Добавить  задачу')
     item3 = KeyboardButton('⚙ Настройки')

     markup.add(item1,item2,item3)
     bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user), reply_markup = markup)


@bot.message_handler(content_types=['text'])
def bot_menu(message):
     chatId = message.chat.id
     waiting_for_message_reply.add(message.chat.id)
     if  message.text == '💌 Список задач':
          bot.send_message(message.chat.id,'Ваш  список  задач:\n')
          for i in range(array.__len__()):
              array[i].getInfo(chatId)

     elif message.text == '💬 Добавить  задачу':
         array.append(example)
         bot.send_message(message.chat.id, 'Введите название задачи:\n')
         array[0].botSetName(message)
         # array[0].botSetContent(message)
         # array[0].botSetDate(message)
         # array[0].botSetTime(message)

     elif message.text == '⚙ Настройки':
          bot.send_message(message.chat.id, 'Пока что  недоступно...\n')
          #здесь  должен запускаться метод для настройки времени

     else:
        bot.send_message(chatId,'Я не знаю что ответить :(')



bot.polling(none_stop=True, interval=0)
