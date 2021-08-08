from app.models import *
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bot.conversationList import *
from telegram.ext import ConversationHandler
from bot.functions import *

def next_to_register(update, context):
    obj = Bot_user.objects.get(user_id=update.message.chat.id)
    if obj.birthday == None:
        update.message.reply_text(get_word('type name', update), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        return SEND_NAME

def send_name(update, context):
    obj = Bot_user.objects.get(user_id=update.message.chat.id)
    obj.name=update.message.text
    obj.save()
    i_contact = KeyboardButton(text=get_word('leave number', update), request_contact=True)
    update.message.reply_text(get_word('send number', update), reply_markup=ReplyKeyboardMarkup([[i_contact]], resize_keyboard=True))
    return SEND_CONTACT

def send_contact(update, context):
    if update.message.contact == None or not update.message.contact:
        update.message.reply_text(get_word('enter button', update))
        return SEND_CONTACT
    else:
        phone_number = update.message.contact.phone_number
    # check that phone is available or no
    is_available = Bot_user.objects.filter(phone=phone_number)
    if is_available:
        update.message.reply_text(get_word('number is logged',update))
        return SEND_CONTACT
    obj = Bot_user.objects.get(user_id=update.message.chat.id)
    obj.phone = phone_number
    obj.save()
    update.message.reply_text(get_word('type data', update), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return SEND_BIRTHDAY

def send_birthday(update, context):
    try:
        # d, m, y = str(update.message.text).split('.')
        l = list(map(int, str(update.message.text).split('.')))
        obj = Bot_user.objects.get(user_id=update.message.chat.id)
        obj.birthday = update.message.text
        obj.save()
        update.message.reply_text(get_word('end login', update))
        main_menu(update, context)
        return ConversationHandler.END
        
    except:
        update.message.reply_text(get_word('error date', update))

