from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from bot.conversationList import *
from bot.functions import *
from app.models import *
from bot.functions import *
from dotenv import load_dotenv
import os

def task_list(update, context):
    bot = context.bot
    # checking that conversition is in proccess or not
    try:
        for dict in context.job_queue._dispatcher.persistence.conversations:
            conv = context.job_queue._dispatcher.persistence.conversations[dict]
            if conv[(update.message.chat.id, update.message.chat.id)] != None and update.message.text != get_word('back', update):
                bot.delete_message(update.message.chat.id, update.message.message_id)
                return
    except:
        do = 0

    all_tasks = Task.objects.filter(is_open=True).order_by('pk')
    for i in Completed_task.objects.filter(user_id=update.message.chat.id):
        all_tasks = all_tasks.exclude(pk=i.task)
    
    items = []
    for i in all_tasks:
        if len(items) <= 10:
            items.append([InlineKeyboardButton(text=str(i.title), callback_data=str(i.pk))])
        else:
            items.append([InlineKeyboardButton(text='➡️', callback_data='next_2')])
            break
    if len(items) == 0:
        update.message.reply_text(get_word('no tasks', update))
        return ConversationHandler.END
    
    items.append([InlineKeyboardButton(text=get_word('back', update), callback_data='back')])
    msg = bot.send_message(update.message.chat.id, get_word('get started', update), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    bot.delete_message(update.message.chat.id, msg.message_id)
    bot.send_message(update.message.chat.id, get_word('get started', update), reply_markup=InlineKeyboardMarkup(items))

    #____create new obj
    Completed_task.objects.create(user_id=update.message.chat.id)
    return SELECT_TASK

def select_task(update, context):
    update = update.callback_query
    bot = context.bot
    data = str(update.data)

    if data == 'back':
        bot.delete_message(update.message.chat.id, update.message.message_id)
        obj = Completed_task.objects.get(user_id=update.message.chat.id, task=None)
        obj.delete()
        main_menu(update, context)
        return ConversationHandler.END
    #_______________________________ Transferring
    if 'index' in data:
        return SELECT_TASK
    if 'next' in data:
        ttt, n = data.split('_') # ttt is word 'next' , n is page number
        tasks = Task.objects.filter(is_open=True).order_by('pk')
        for i in Completed_task.objects.filter(user_id=update.message.chat.id):
            tasks = tasks.exclude(pk=i.task)
        breaknvalues = (int(n) - 1) * 11
        ls = [] # new list
        for i in tasks[breaknvalues:]:
            if len(ls) <= 10:
                ls.append([InlineKeyboardButton(text=str(i.title), callback_data=str(i.pk))])
            else:
                nn = str(int(n)+1) # next n 
                pn = str(int(n)-1) # previous n
                if pn == '0':
                    ls.append([InlineKeyboardButton(text=n, callback_data='index'), InlineKeyboardButton(text='➡️', callback_data='next_{}'.format(nn))])
                else:
                    ls.append([InlineKeyboardButton(text='⬅️', callback_data='previous_{}'.format(pn)), InlineKeyboardButton(text=n, callback_data='index'), InlineKeyboardButton(text='➡️', callback_data='next_{}'.format(nn))])
                break
        else:
            pn = str(int(n) - 1)
            if pn != 0:
                ls.append([InlineKeyboardButton(text='⬅️', callback_data='previous_{}'.format(pn)), InlineKeyboardButton(text=n, callback_data='index')])
        ls.append([InlineKeyboardButton(text=get_word('back', update), callback_data='back')])
        update.edit_message_text(get_word('get started', update), reply_markup=InlineKeyboardMarkup(ls))
        return SELECT_TASK
    if 'previous' in data:
        ttt, n = data.split('_') # n is page number
        breaknvalues = (int(n) - 1) * 9
        tasks = Task.objects.filter(is_open=True).order_by('pk')
        for i in Completed_task.objects.filter(user_id=update.message.chat.id):
            tasks = tasks.exclude(pk=i.task)
        ls = []
        for i in tasks:
            if len(ls) <= 10:
                ls.append([InlineKeyboardButton(text=str(i.title), callback_data=str(i.pk))])
            else:
                nn = str(int(n)+1) # next n 
                pn = str(int(n)-1) # previous n
                if pn == '0':
                    ls.append([InlineKeyboardButton(text=n, callback_data='index'), InlineKeyboardButton(text='➡️', callback_data='next_{}'.format(nn))])
                else:
                    ls.append([InlineKeyboardButton(text='⬅️', callback_data='previous_{}'.format(pn)), InlineKeyboardButton(text=n, callback_data='index'), InlineKeyboardButton(text='➡️', callback_data='next_{}'.format(nn))])
                break
        else:
            pn = str(int(n) - 1)
            if pn != 0:
                ls.append([InlineKeyboardButton(text='⬅️', callback_data='previous_{}'.format(pn)), InlineKeyboardButton(text=n, callback_data='index')])
        ls.append([InlineKeyboardButton(text=get_word('back', update), callback_data='back')])
        
        update.edit_message_text(get_word('get started', update), reply_markup=InlineKeyboardMarkup(ls))
        return SELECT_TASK
    
    #___________________________________________________________
    # selecting the task

    bot.delete_message(update.message.chat.id, update.message.message_id)
    task = Task.objects.get(pk=int(data))
    text = task.description + '\n' + task.url + '\n\n{}:'.format(get_word('price', update)) + str(task.price)
    #i_link = InlineKeyboardButton(text='Начать', url=task.url)
    if task.photo != '':
        try:
            bot.send_photo(update.message.chat.id, task.photo)
        except:
            qwqwq = 0
    bot.send_message(update.message.chat.id, text)
    bot.send_message(update.message.chat.id, get_word('after ending task', update), reply_markup=ReplyKeyboardMarkup(keyboard=[['🏁☑️'], [get_word('back', update)]], resize_keyboard=True))

    # set data
    obj = Completed_task.objects.get(user_id=update.message.chat.id, task=None)
    obj.task = int(data)
    obj.save()
    return SEND_PROOF


def send_proof(update, context):
    if update.message.text == get_word('back', update):
        try:
            obj = Completed_task.objects.get(user_id=update.message.chat.id, photo='')
            obj.delete()
        except:
            do = 0
        task_list(update, context)
        return SELECT_TASK
    
    update.message.reply_text(get_word('send proof', update), reply_markup=ReplyKeyboardMarkup(keyboard=[[get_word('back', update)]], resize_keyboard=True))
    return SEND_PROOF_PHOTO

def send_proof_photo(update, context):
    bot = context.bot
    try:
        obj = Completed_task.objects.get(user_id=update.message.chat.id, photo='')
        task  = Task.objects.get(pk=obj.task)
        task.done += 1
        task.save()
        if task.done == task.limit:
            task.done = 0
            task.is_open = False
            task.save()
        p = bot.getFile(update.message.photo[-1].file_id)
        *args, file_name = str(p.file_path).split('/')
        d_photo = p.download('files/photos/completed_tasks/{}'.format(file_name))
        obj.photo = str(d_photo).replace('files/', '')
        obj.save()
        update.message.reply_text(get_word('end task', update))
        main_menu(update, context)
        return ConversationHandler.END
    
        
    except:
        if update.message.text == get_word('back', update):
            try:
                obj = Completed_task.objects.get(user_id=update.message.chat.id, photo='')
                obj.delete()
            except:
                do = 0
            task_list(update, context)
            return SELECT_TASK

