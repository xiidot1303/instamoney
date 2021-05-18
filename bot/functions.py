from telegram import ReplyKeyboardMarkup, KeyboardButton

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
    bot.send_message(update.message.chat.id, 'Главное меню', reply_markup=ReplyKeyboardMarkup(keyboard=[['Доступные задания 📝'], ['Вывод 📥'], ['Баланс 💰'], ['Служба поддержки ⚙️']], resize_keyboard=True))

