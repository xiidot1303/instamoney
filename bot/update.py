from telegram import Bot
from telegram.ext import Dispatcher, ConversationHandler
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
if WHERE == 'SERVER':
    updater = 1213
    dp = Dispatcher(bot_obj, None, workers=0, use_context=True)
else:
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

# delete un completed objects ones, after restart
c_task = Completed_task.objects.filter(photo='')
output = Output.objects.filter(price=None)
user = Bot_user.objects.filter(birthday=None)
for i in c_task:
    i.delete()
for i in output:
    i.delete()
for i in user:
    i.delete()




login_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(['продолжить']), next_to_register)],
    states={
        SEND_NAME: [MessageHandler(Filters.text, send_name)],
        SEND_CONTACT: [MessageHandler(Filters.contact, send_contact), MessageHandler(Filters.text, send_contact)],
        SEND_BIRTHDAY: [MessageHandler(Filters.text, send_birthday)],


    },
    fallbacks = [],
)

begin_task = ConversationHandler(
    entry_points = [MessageHandler(Filters.text(['Доступные задания 📝']), task_list)], 
    states = {
        SELECT_TASK: [CallbackQueryHandler(select_task)],
        SEND_PROOF: [MessageHandler(Filters.text(['🏁☑️', 'Назад']), send_proof)],
        SEND_PROOF_PHOTO: [MessageHandler(Filters.photo, send_proof_photo), MessageHandler(Filters.text(['Назад']), send_proof_photo)],
    }, 
    fallbacks = [CommandHandler('cancel', cancel)],
)

output_request = ConversationHandler(
    entry_points = [MessageHandler(Filters.text(['Вывод 📥']), request_money)], 
    states = {
        SEND_OUTPUT_DESCRIPTION: [MessageHandler(Filters.text, send_output_description)],
        SEND_OUTPUT_PRICE: [MessageHandler(Filters.text, send_output_price)],
    }, 
    fallbacks = [CommandHandler('cancel', cancel)],
    )

dp.add_handler(CommandHandler('start', start))
dp.add_handler(login_handler)
dp.add_handler(begin_task)
dp.add_handler(output_request)
dp.add_handler(MessageHandler(Filters.text(['Баланс 💰']), balance))
dp.add_handler(MessageHandler(Filters.text(['Служба поддержки ⚙️']), service_support))
dp.add_handler(CommandHandler('cancel', cancel))