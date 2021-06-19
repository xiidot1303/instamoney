from telegram import ReplyKeyboardMarkup, KeyboardButton
from bot.uz_ru import lang_dict
from app.models import *

def is_registered(id):
    if Bot_user.objects.filter(user_id=id):
        return True
    else:
        return False

def main_menu(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www= 0 # do nothing
    
    bot = context.bot
    bot.send_message(update.message.chat.id, get_word('main menu', update), reply_markup=ReplyKeyboardMarkup(keyboard=[[get_word('tasks', update)], [get_word('output', update)], [get_word('balance', update)], [get_word('support', update)]], resize_keyboard=True))

def get_word(text, update):
    user = Bot_user.objects.get(user_id=update.message.chat.id)
    if user.lang == 'uz':
        return lang_dict[text][0]
    else:
        return lang_dict[text][1]