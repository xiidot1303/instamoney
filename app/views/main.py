from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from bot.update import dp, updater
from django.http import HttpResponse, FileResponse
from dotenv import load_dotenv
import os
from app.models import *
import requests
import json
from django.contrib.auth.decorators import login_required

basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
WHERE = os.environ.get('WHERE')


@csrf_exempt
def bot_webhook(request):

    if WHERE == 'LOCAL':
        updater.start_polling()
    else:
        update = Update.de_json(json.loads(request.body.decode('utf-8')), dp.bot)
        dp.process_update(update)
    return HttpResponse('Bot started!')


@login_required
def turn_on_off_task(request, pk):
    task = Task.objects.get(pk=pk)
    if task.is_open:
        task.is_open = False
    else:
        task.is_open = True
    task.save()
    return redirect(all_tasks)

@login_required
def all_tasks(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'views/all_tasks.html', context)


@login_required
def completed_tasks(request, task):
    if task == 0:
        tasks = Completed_task.objects.exclude(photo='')
    else:
        tasks = Completed_task.objects.filter(task=task).exclude(photo='')
    phone_numbers = [Bot_user.objects.get(user_id=i.user_id).phone for i in tasks]
    names = [Bot_user.objects.get(user_id=i.user_id).name for i in tasks]
    birthdays = [Bot_user.objects.get(user_id=i.user_id).birthday for i in tasks]
    context = {'task': task, 'tasks': tasks, 'phone_numbers': phone_numbers, 'names': names, 'birthdays': birthdays}
    return render(request, 'views/completed_tasks.html', context)

@login_required
def outputs(request):
    objs = Output.objects.exclude(price=None)
    phone_numbers = [Bot_user.objects.get(user_id=i.user_id).phone for i in objs]
    names = [Bot_user.objects.get(user_id=i.user_id).name for i in objs]
    birthdays = [Bot_user.objects.get(user_id=i.user_id).birthday for i in objs]
    context = {'objs': objs, 'phone_numbers': phone_numbers, 'names': names, 'birthdays': birthdays}
    return render(request, 'views/outputs.html', context)

def view_output(request, pk):
    obj = Output.objects.get(pk=pk)
    user = Bot_user.objects.get(user_id=obj.user_id)
    context = {'obj': obj, 'user': user}
    return render(request, 'views/view_output.html', context)