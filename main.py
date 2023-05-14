import telegram
from telegram.ext import Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler
import datetime
import logging
import threading
from TOKEN import chatId

semaphore = threading.Semaphore(1)



notes = []
bot = telegram.Bot(token="6107959341:AAG_5x7Hi3oJRWAG47l9uGMAmVJIUH_DfGI")


class Note:
    def __init__(self):
        self.name = None
        self.content = None
        self.date = None
        self.time = None

    def get_info(self):
        if self.date is None and self.time is None:
            return f"{self.name}\n{self.content}\n"
        else:
            return f"{self.name}\n{self.content}\nДата отправки: {self.date}\nВремя отправки: {self.time}\n"

    def send_reminders(self):
        bot.send_message(chat_id = chatId, text=f'Напоминание по заметке "{self.name}":\n{self.content}')
        self.date = None  # обновляем состояние заметки после отправки уведомления
        self.time = None

def start(update,context):
    button = [
        [InlineKeyboardButton('Создать заметку', callback_data='CREATE')],
    ]
    keyBoard = InlineKeyboardMarkup(button)
    update.message.reply_text('Привет! Я бот для создания заметок.Вот список моих команд:\n/list - вывести список заметок\n/create - создать заметку\n/start - перейти в начало\nЧтобы начать, нажмите "Создать заметку".', reply_markup=keyBoard)
    return "CHOOSING_ACTION1"

def createComm(update,context):
    bot.send_message(chat_id = chatId, text='Введите имя заметки:')
    return "CREATE_NOTE_STEP1"

def create_note_step1(update, context):
    note = Note()
    note.name = update.message.text
    context.user_data['note'] = note
    update.message.reply_text('Введите содержание заметки:')
    return "CREATE_NOTE_STEP2"

def create_note_step2(update, context):
    note = context.user_data['note']
    note.content = update.message.text
    yes_no = [[InlineKeyboardButton('Да', callback_data='Yes')],
              [InlineKeyboardButton('Нет', callback_data='No')],
              ]

    reply_keyboard = InlineKeyboardMarkup(yes_no)
    update.message.reply_text('Хотите указать дату и время отправки заметки?', reply_markup=reply_keyboard)
    return "CHOOSING_ACTION2"

def create_note_step4(update, context):
    try:
        date = datetime.datetime.strptime(update.message.text, '%d.%m.%Y')
        note = context.user_data['note']
        note.date = update.message.text
        update.message.reply_text('Введите время отправки в формате чч:мм:')
        return "CREATE_NOTE_STEP5"
    except ValueError:
        update.message.reply_text('Некорректный формат даты. Попробуйте снова.')
        return "CREATE_NOTE_STEP4"

def create_note_step5(update, context):
    try:
        time = datetime.datetime.strptime(update.message.text, '%H:%M')
        note = context.user_data['note']
        note.time = update.message.text
        notes.append(note)
        update.message.reply_text('Заметка успешно создана!\nВот ваша заметка:\n' + note.get_info())
        note.get_info()
        return ConversationHandler.END
    except ValueError:
        update.message.reply_text('Некорректный формат времени. Попробуйте снова.')
        return "CREATE_NOTE_STEP5"


def check_notes(job):
    now = datetime.datetime.now()
    for note in notes:
        if note.date and note.time:
            note_time = datetime.datetime.strptime(note.date + ' ' + note.time, '%d.%m.%Y %H:%M')
            if note_time <= now:
                note.send_reminders()


def list_notes(update, context):
    if len(notes) == 0:
        bot.send_message(chat_id= chatId, text='Список заметок пуст.')
    else:
        for note in notes:
            bot.send_message(chat_id= chatId, text=note.get_info())

def cancel(update, context):
    update.message.reply_text('Действие отменено.')
    return ConversationHandler.END



# Создание logger
logger = logging.getLogger(__name__)
# Установка уровня логирования
logger.setLevel(logging.INFO)
# Создание консольного обработчика логов
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# Форматирование сообщений
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
# Добавление обработчика логов в logger
logger.addHandler(console_handler)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)



def keyboard(update, context):
    query = update.callback_query
    action = query.data
    if action == 'CREATE':
        bot.send_message(chat_id='858820475', text='Введите имя заметки:', reply_markup=None)
        return "CREATE_NOTE_STEP1"
    elif action == "Yes":
        query.message.reply_text('Введите дату отправки в формате дд.мм.гггг:')
        context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        return "CREATE_NOTE_STEP4"
    elif action == "No":
        note = context.user_data['note']
        notes.append(note)
        query.message.reply_text('Заметка успешно создана!\n' + note.get_info())
        context.bot.edit_message_reply_markup(chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=None)
        return ConversationHandler.END


def main():
    updater = Updater(token="6107959341:AAG_5x7Hi3oJRWAG47l9uGMAmVJIUH_DfGI", use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            "CHOOSING_ACTION1": [CallbackQueryHandler(keyboard)],
            "CREATE_NOTE_STEP1": [MessageHandler(Filters.text & ~Filters.command, create_note_step1)],
            "CREATE_NOTE_STEP2": [MessageHandler(Filters.text & ~Filters.command, create_note_step2)],
            "CHOOSING_ACTION2": [CallbackQueryHandler(keyboard)],
            "CREATE_NOTE_STEP4": [MessageHandler(Filters.text & ~Filters.command, create_note_step4)],
            "CREATE_NOTE_STEP5": [MessageHandler(Filters.text & ~Filters.command, create_note_step5)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    create_handler = ConversationHandler(
        entry_points=[CommandHandler('create', createComm)],
        states={
            "CREATE_NOTE_STEP1": [MessageHandler(Filters.text & ~Filters.command, create_note_step1)],
            "CREATE_NOTE_STEP2": [MessageHandler(Filters.text & ~Filters.command, create_note_step2)],
            "CHOOSING_ACTION2": [CallbackQueryHandler(keyboard)],
            "CREATE_NOTE_STEP4": [MessageHandler(Filters.text & ~Filters.command, create_note_step4)],
            "CREATE_NOTE_STEP5": [MessageHandler(Filters.text & ~Filters.command, create_note_step5)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    job_queue = updater.job_queue
    job_queue.run_repeating(check_notes, interval=0, context = job_queue)
    job_queue.start()
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(create_handler)
    updater.dispatcher.add_handler(CommandHandler('list', list_notes))
    updater.dispatcher.add_handler(CallbackQueryHandler(keyboard))
    updater.dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
