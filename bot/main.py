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
        update.message.reply_text('Приветствую. Это бот для заработка в Инстаграмме. Тут будут появляться задания, выполнив которые вы будете получать вознаграждение. Цены за задания варируются от 200 до 1000 сумм. Минимальная сумма для вывода: 5000 сумм. Выводим на узкард. Успехов!', reply_markup=ReplyKeyboardMarkup(keyboard=[['продолжить']], resize_keyboard=True))


def balance(update, context):
    user = Bot_user.objects.get(user_id=update.message.chat.id)
    update.message.reply_text('Ваш баланс:\n\n{} сумм'.format(user.balance))

def cancel(update, context):
    bot = context.bot
    if not Bot_user.objects.filter(user_id=update.message.chat.id):
        c_task = Completed_task.objects.filter(photo='', user_id=update.message.chat.id)
        output = Output.objects.filter(price=None, user_id=update.message.chat.id)

        for i in c_task:
            i.delete()
        for i in output:
            i.delete()
        

        get = update.message.reply_text('Нажмите /start для повторного входа в бота', reply_markup=ReplyKeyboardMarkup(keyboard=[['/start']], resize_keyboard=True))
        bot.delete_message(update.message.chat.id, get.message_id-2)
        bot.delete_message(update.message.chat.id, get.message_id-1)
        return ConversationHandler.END

def service_support(update, context):
    update.message.reply_text('Если у вас возникли вопросы или проблемы, пожалуйста свяжитесь с администратором\n\n@Gleb_ForexMaster')