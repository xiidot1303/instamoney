from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from app.models import *
from app.views.main import *
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
import os
import telegram
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')



@login_required
def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    for c in Completed_task.objects.filter(task=pk):
        c.delete()
    task.delete()
    return redirect(all_tasks)

def delete_user(request, pk, redirect_filter):
    bot_user = Bot_user.objects.get(pk=pk)

    # send message to user
    bot = telegram.Bot(token=TOKEN)
    try:
        get = bot.sendMessage(chat_id=bot_user.user_id, text='Ваш профиль удален\nНажмите /cancel', reply_markup=ReplyKeyboardMarkup(keyboard=[['/cancel']], resize_keyboard=True))
    except:
        dedfedf = 0
    bot_user.delete()
    return redirect(bot_users, filter=redirect_filter)
    
