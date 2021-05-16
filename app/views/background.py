from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from app.models import *
from app.views.main import *
from dotenv import load_dotenv
import os
import telegram
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')
from dotenv import load_dotenv
import os
import telegram
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')



def done_task(request, id, redirect_id, user):
    c_task = Completed_task.objects.get(pk=id) # get completed task that should delete
    bot_user = Bot_user.objects.get(user_id=c_task.user_id) # current bot user that created current task
    
    task = Task.objects.get(pk=c_task.task)   # get current task
    bot_user.balance += task.price
    bot_user.c_task += 1
    bot_user.save()
    c_task.status = 'done'
    c_task.save()
    # send message to user
    bot = telegram.Bot(token=TOKEN)
    try:
        bot.sendMessage(chat_id=bot_user.user_id, text='Ваша задача выполнена')
    except:
        www = 0 # do nothing
    
    return redirect(completed_tasks, task=redirect_id, user_and_phone=user)

def denied_task(request, id, redirect_id, user):
    c_task = Completed_task.objects.get(pk=id) # get completed task that should delete
    bot_user = Bot_user.objects.get(user_id=c_task.user_id) # current bot user that created current task
    c_task.status = 'denied'
    c_task.save()
    # send message to user
    bot = telegram.Bot(token=TOKEN)
    try:
        bot.sendMessage(chat_id=bot_user.user_id, text='Ваша задача отклонена')
    except:
        www = 0 # do nothing
    
    return redirect(completed_tasks, task=redirect_id, user_and_phone=user)


def allow_output(request, pk):
    obj = Output.objects.get(pk=pk)
    user = Bot_user.objects.get(user_id=obj.user_id)
    user.balance -= obj.price
    user.save()
    # send message to user
    bot = telegram.Bot(token=TOKEN)
    try:
        bot.sendMessage(chat_id=user.user_id, text='{} выведено с вашего счета'.format(str(obj.price)))
    except:
        www = 0 # do nothing
    obj.delete()
    return redirect(outputs)



def deny_output(request, pk):
    obj = Output.objects.get(pk=pk)
    user = Bot_user.objects.get(user_id=obj.user_id)

    # send message to user
    bot = telegram.Bot(token=TOKEN)
    try:
        bot.sendMessage(chat_id=user.user_id, text='Ваш запрос на вывод денег был отменен')
    except:
        www = 0 # do nothing
    obj.delete()
    return redirect(outputs)