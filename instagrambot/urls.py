"""instagrambot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView
from app.views.main import *
from app.views.create import *
from app.views.detail import *
from app.views.delete import *
from app.views.update import *
from app.views.file import *
from app.views.background import *
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view()),
    path('', all_tasks),
    #start bot
    path(TOKEN, bot_webhook, name='bot'),
    
    #file response
    path('files/photos/<str:folder>/<str:file>/', get_photos, name='get_photo'),
    

    #background
    path('done_task/<int:id>/<int:redirect_id>/<str:user>/', done_task, name='done_task'),
    path('denied_task/<int:id>/<int:redirect_id>/<str:user>/', denied_task, name='denied_task'),

    path('allow_output/<int:pk>/', allow_output, name = 'allow_output'),
    path('deny_output/<int:pk>/', deny_output, name = 'deny_output'),

    # task
    path('create_task', TaskCreateView.as_view(), name='create_task'), # create new task
    path('task_detail/<int:pk>/', TaskDetailView.as_view()),  # details after creating new task
    path('all_tasks', all_tasks, name='all_tasks'), # all task list
    path('delete_task/<int:pk>/', delete_task, name='delete_task'), #delete task by pk
    path('update_task/<int:pk>/', TaskEditView.as_view(), name='update_task'),
        # turn on off task
    path('turn_on_of_task/<int:pk>/', turn_on_off_task, name='turn_on_off_task'),

    #completed_task
    path('completed_task/<int:task>/<str:user_and_phone>/', completed_tasks, name='completed_task'),

    #Output
    path('outputs', outputs, name='outputs'),
    path('view_output/<int:pk>/', view_output, name='view_output'),

    #Bot users
    path('bot_users/<str:filter>/', bot_users, name='bot_users'), #the list of bot users
    path('delete_user/<int:pk>/<str:redirect_filter>/', delete_user, name='delete_user'),

    #checked task
    path('checked_tasks/<int:user>/', checked_tasks, name='checked_tasks'),
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
