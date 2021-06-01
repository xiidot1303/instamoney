from django.forms.utils import pretty_name
from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from app.models import *
from app.views.main import *
from app.forms import *
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




@login_required
def sendmessage(request, issent):
    if request.method == 'POST':
        bbf = SendmessageForm(request.POST, request.FILES)
        if bbf.is_valid():
            print('heyy')
            if bbf.cleaned_data['select'] == 'Все':
                msg = bbf.cleaned_data['message']
                photo = bbf.cleaned_data['photo']
                users = Bot_user.objects.all()
                for u in users:
                    my_token = TOKEN
                    bot = telegram.Bot(token=my_token)
                    try:
                        bot.sendPhoto(chat_id=u.user_id, photo=photo, caption=msg)
                    except:
                        fewfwe = 0

            else:
                name_and_phone = bbf.cleaned_data['select']
                msg = bbf.cleaned_data['message']
                photo = bbf.cleaned_data['photo']
                *name_args, phone = str(name_and_phone).split()
                name = ''
                for i in name_args:
                    name += ' ' + i
                name = name[1:]
                objs = Bot_user.objects.filter(name=name, phone=phone)
                user_id = objs[0].user_id
                my_token = TOKEN


                bot = telegram.Bot(token=my_token)
                try:
                    bot.sendPhoto(chat_id=user_id, photo=photo, caption=msg)
                except:
                    qw = 0
                return redirect(sendmessage, issent='yes')
            
            
            return redirect(sendmessage, issent='yes')
            
        else:
            profiles = Bot_user.objects.all()

            context = {'form': bbf, 'profiles': profiles, 'issent': issent}
            return render(request, 'views/sendmessage.html', context)

    else:
        bbf = SendmessageForm()
        profiles = Bot_user.objects.all()

        context = {'form': bbf, 'profiles': profiles, 'issent': issent}
        return render(request, 'views/sendmessage.html', context)    

