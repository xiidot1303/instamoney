from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from bot.conversationList import *
from bot.functions import *

from app.models import *
from bot.functions import *
from dotenv import load_dotenv
import os



def request_money(update, context):
    # delete unfinished objects
    del_msg = Output.objects.filter(price=None, user_id=update.message.chat.id)
    for i in del_msg:
        i.delete()
    #___________________________
    Output.objects.create(user_id=update.message.chat.id)
    update.message.reply_text('Отправьте реквизиты', reply_markup=ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
    return SEND_OUTPUT_DESCRIPTION

def send_output_description(update, context):
    if update.message.text == 'Назад':
        obj = Output.objects.get(user_id=update.message.chat.id, description=None)
        obj.delete()
        main_menu(update, context)
        return ConversationHandler.END
    obj = Output.objects.get(user_id=update.message.chat.id, description=None)
    obj.description=update.message.text
    obj.save()
    update.message.reply_text('Введите сумму денег', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return SEND_OUTPUT_PRICE

def send_output_price(update, context):
    obj = Output.objects.get(user_id=update.message.chat.id)
    obj.price = float(update.message.text)
    obj.save()
    update.message.reply_text('Ваша заявка принята и проходит модерацию')
    main_menu(update, context)
    return ConversationHandler.END

    