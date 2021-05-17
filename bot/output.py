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
    update.message.reply_text('Введите номер вашей карты', reply_markup=ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
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
    update.message.reply_text('Введите сумму, которую вы хотите вывести', reply_markup=ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
    return SEND_OUTPUT_PRICE

def send_output_price(update, context):
    if update.message.text == 'Назад':
        request_money(update, context)
        return SEND_OUTPUT_DESCRIPTION
    try:
        if Bot_user.objects.get(user_id=update.message.chat.id).balance < float(update.message.text):
            update.message.reply_text('Недостаточно сумма\nВведите другую сумму')
            return SEND_OUTPUT_PRICE
        obj = Output.objects.get(user_id=update.message.chat.id, price=None)
        obj.price = float(update.message.text)
        obj.save()
        update.message.reply_text('Ваша заявка на вывод денег принята и находится на проверке. Вы получите ответ, сразу после проверки администратором.')
        main_menu(update, context)
        return ConversationHandler.END

    except:
        update.message.reply_text('Введите сумму!')
        return SEND_OUTPUT_PRICE