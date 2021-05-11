from app.models import *
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bot.conversationList import *
from telegram.ext import ConversationHandler
from bot.functions import *

def next_to_register(update, context):
    if not is_registered(update.message.chat.id):
        update.message.reply_text('Введите ваше ФИО', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        return SEND_NAME

def send_name(update, context):
    obj = Bot_user.objects.create(user_id=update.message.chat.id, name=update.message.text)
    i_contact = KeyboardButton(text='Оставить номер телефона', request_contact=True)
    update.message.reply_text('Оставьте свой номер телефона', reply_markup=ReplyKeyboardMarkup([[i_contact]], resize_keyboard=True))
    return SEND_CONTACT

def send_contact(update, context):
    if update.message.contact == None or not update.message.contact:
        phone_number = update.message.text
    else:
        phone_number = update.message.contact.phone_number
    # check that phone is available or no
    is_available = Bot_user.objects.filter(phone=phone_number)
    if is_available:
        update.message.reply_text('Этот номер уже зарегистрирован. Введите другой номер')
        return SEND_CONTACT
    obj = Bot_user.objects.get(user_id=update.message.chat.id)
    obj.phone = phone_number
    obj.save()
    update.message.reply_text('Введите вашу дату рождения в формате дд.мм.ггг', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return SEND_BIRTHDAY

def send_birthday(update, context):
    try:
        d, m, y = str(update.message.text).split('.')
        obj = Bot_user.objects.get(user_id=update.message.chat.id)
        obj.birthday = update.message.text
        obj.save()
        update.message.reply_text('Вы успешно зарегистрировались')
        main_menu(update, context)
        return ConversationHandler.END
        
    except:
        update.message.reply_text('Введите в формате дд.мм.ггг')

