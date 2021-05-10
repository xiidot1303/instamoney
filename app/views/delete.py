from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from app.models import *
from app.views.main import *
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
import os


@login_required
def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    for c in Completed_task.objects.filter(task=pk):
        c.delete()
    task.delete()
    return redirect(all_tasks)