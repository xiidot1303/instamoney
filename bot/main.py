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
        update.message.reply_text('Описание бота', reply_markup=ReplyKeyboardMarkup(keyboard=[['продолжить']], resize_keyboard=True))


def balance(update, context):
    user = Bot_user.objects.get(user_id=update.message.chat.id)
    update.message.reply_text('Ваш баланс:\n\n{}'.format(user.balance))