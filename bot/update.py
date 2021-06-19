from telegram import Bot
from telegram.ext import Dispatcher, ConversationHandler, PicklePersistence
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from bot.main import *
from bot.login import *
from bot.output import *
from bot.conversationList import *
from bot.task import *
from dotenv import load_dotenv
import os
from app.models import *
basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')
WHERE = os.environ.get('WHERE')
bot_obj = Bot(TOKEN)
persistence = PicklePersistence(filename='filebot')
if WHERE == 'SERVER':
    updater = 1213
    dp = Dispatcher(bot_obj, None, workers=0, use_context=True, persistence=persistence)
else:
    
    updater = Updater(token=TOKEN, use_context=True, persistence=persistence)
    dp = updater.dispatcher





login_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(['продолжить', 'davom etish']), next_to_register)],
    states={
        SEND_NAME: [MessageHandler(Filters.text, send_name)],
        SEND_CONTACT: [MessageHandler(Filters.contact, send_contact), MessageHandler(Filters.text, send_contact)],
        SEND_BIRTHDAY: [MessageHandler(Filters.text, send_birthday)],


    },
    fallbacks = [],
    name='login',
    persistent=True,
)

begin_task = ConversationHandler(
    entry_points = [MessageHandler(Filters.text(['Доступные задания 📝', 'Mavjud vazifalar 📝']), task_list)], 
    states = {
        SELECT_TASK: [CallbackQueryHandler(select_task)],
        SEND_PROOF: [MessageHandler(Filters.text(['🏁☑️', 'Назад', 'Ortga']), send_proof)],
        SEND_PROOF_PHOTO: [MessageHandler(Filters.photo, send_proof_photo), MessageHandler(Filters.text(['Назад', 'Ortga']), send_proof_photo)],
    }, 
    fallbacks = [CommandHandler('cancel', cancel)],
    name='task',
    persistent=True,
)

output_request = ConversationHandler(
    entry_points = [MessageHandler(Filters.text(['Вывод 📥', 'Mablag\'ni yechib olish 📥']), request_money)], 
    states = {
        SEND_OUTPUT_DESCRIPTION: [MessageHandler(Filters.text, send_output_description)],
        SEND_OUTPUT_PRICE: [MessageHandler(Filters.text, send_output_price)],
    }, 
    fallbacks = [CommandHandler('cancel', cancel)],
    name='output',
    persistent=True,
    )

dp.add_handler(CommandHandler('start', start))
dp.add_handler(login_handler)
dp.add_handler(begin_task)
dp.add_handler(output_request)
dp.add_handler(MessageHandler(Filters.text(['Баланс 💰', 'Balans 💰']), balance))
dp.add_handler(MessageHandler(Filters.text(['Служба поддержки ⚙️', 'Yordam xizmati ⚙️']), service_support))
dp.add_handler(CommandHandler('cancel', cancel))