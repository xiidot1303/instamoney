from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from app.forms import *
from app.models import *



class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'detail/task_detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = context['object']
      
        context['ID'] = obj.pk
        return context
