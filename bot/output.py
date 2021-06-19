from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from bot.conversationList import *
from bot.functions import *
from bot.main import cancel
from app.models import *
from bot.functions import *
from dotenv import load_dotenv
import os



def request_money(update, context):
    bot = context.bot
    # checking that conversition is in proccess or not
    try:
        for dict in context.job_queue._dispatcher.persistence.conversations:
            conv = context.job_queue._dispatcher.persistence.conversations[dict]
            if conv[(update.message.chat.id, update.message.chat.id)] != None and update.message.text != get_word('back', update):
                bot.delete_message(update.message.chat.id, update.message.message_id)
                return
    except:
        do = 0
    # delete unfinished objects
    del_msg = Output.objects.filter(price=None, user_id=update.message.chat.id)
    for i in del_msg:
        i.delete()
    #___________________________
    Output.objects.create(user_id=update.message.chat.id)
    update.message.reply_text(get_word('type card number', update), reply_markup=ReplyKeyboardMarkup(keyboard=[[get_word('back', update)]], resize_keyboard=True))
    return SEND_OUTPUT_DESCRIPTION
    

def send_output_description(update, context):
    if update.message.text == '/cancel':
        cancel(update, context)
        return ConversationHandler.END
    
    if update.message.text == get_word('back', update):
        obj = Output.objects.get(user_id=update.message.chat.id, description=None)
        obj.delete()
        main_menu(update, context)
        return ConversationHandler.END
    obj = Output.objects.get(user_id=update.message.chat.id, description=None)
    obj.description=update.message.text
    obj.save()
    update.message.reply_text(get_word('type output value', update), reply_markup=ReplyKeyboardMarkup(keyboard=[[get_word('back', update)]], resize_keyboard=True))
    return SEND_OUTPUT_PRICE

def send_output_price(update, context):
    if update.message.text == '/cancel':
        cancel(update, context)
        return ConversationHandler.END
    if update.message.text == get_word('back', update):
        request_money(update, context)
        return SEND_OUTPUT_DESCRIPTION
    try:
        if Bot_user.objects.get(user_id=update.message.chat.id).balance < float(update.message.text):
            update.message.reply_text(get_word('insufficient amount', update))
            return SEND_OUTPUT_PRICE
        obj = Output.objects.get(user_id=update.message.chat.id, price=None)
        obj.price = float(update.message.text)
        obj.save()
        update.message.reply_text(get_word('end output', update))
        main_menu(update, context)
        return ConversationHandler.END

    except:
        update.message.reply_text(get_word('type value', update))
        return SEND_OUTPUT_PRICE