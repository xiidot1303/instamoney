from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from app.forms import *
from app.models import *

class TaskCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create/create_task.html'
    form_class = TaskForm
    success_url = '/task_detail/{id}'
    permanent = True
