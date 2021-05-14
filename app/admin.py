from django.contrib import admin
from app.models import *


class Bot_userAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'balance')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'url', 'description', 'price')

class Completed_taskAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'task', 'date')

class OutputAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'price')

admin.site.register(Bot_user, Bot_userAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Completed_task, Completed_taskAdmin)
admin.site.register(Output, OutputAdmin)