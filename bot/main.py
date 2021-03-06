from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from bot.conversationList import *
from bot.functions import *
from app.models import *
from bot.functions import *
from dotenv import load_dotenv
import os


def start(update, context):
    if is_registered(update.message.chat.id):
        c_task = Completed_task.objects.filter(user_id=update.message.chat.id, photo='')
        output = Output.objects.filter(user_id=update.message.chat.id, price=None)
        user = Bot_user.objects.filter(user_id=update.message.chat.id, birthday=None)
        if not c_task and not output and not user:
            main_menu(update, context)
        else:
            bot = context.bot
            bot.delete_message(update.message.chat.id, update.message.message_id)
    else:
        Bot_user.objects.create(user_id=update.message.chat.id)
        update.message.reply_text(get_word('welcome', update), reply_markup=ReplyKeyboardMarkup(keyboard=[[get_word('next', update)]], resize_keyboard=True))
        

def balance(update, context):
    bot = context.bot
    # checking that conversition is in proccess or not
    try:
        for dict in context.job_queue._dispatcher.persistence.conversations:
            conv = context.job_queue._dispatcher.persistence.conversations[dict]
            if conv[(update.message.chat.id, update.message.chat.id)] != None:
                bot.delete_message(update.message.chat.id, update.message.message_id)
                return
    except:
        do = 9
    user = Bot_user.objects.get(user_id=update.message.chat.id)
    update.message.reply_text('{}:\n\n{} {}'.format(get_word('your balance', update), user.balance, get_word('summ', update)))

def cancel(update, context):
    bot = context.bot
    if not Bot_user.objects.filter(user_id=update.message.chat.id):
        c_task = Completed_task.objects.filter(photo='', user_id=update.message.chat.id)
        output = Output.objects.filter(price=None, user_id=update.message.chat.id)

        for i in c_task:
            i.delete()
        for i in output:
            i.delete()
        

        get = update.message.reply_text('Qaytatdan kirish uchun /start tugmasini bosing\n\n?????????????? /start ?????? ???????????????????? ?????????? ?? ????????', reply_markup=ReplyKeyboardMarkup(keyboard=[['/start']], resize_keyboard=True))
        bot.delete_message(update.message.chat.id, get.message_id-2)
        bot.delete_message(update.message.chat.id, get.message_id-1)
        return ConversationHandler.END
    else:
        bot.delete_message(update.message.chat.id, update.message.message_id)
def service_support(update, context):
    bot = context.bot
    # checking that conversition is in proccess or not

    try:
        for dict in context.job_queue._dispatcher.persistence.conversations:
            conv = context.job_queue._dispatcher.persistence.conversations[dict]
            if conv[(update.message.chat.id, update.message.chat.id)] != None:
                bot.delete_message(update.message.chat.id, update.message.message_id)
                return
    except:
        do = 0
    update.message.reply_text(get_word('support text', update))