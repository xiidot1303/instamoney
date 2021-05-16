from django.db import models

class Bot_user(models.Model):
    user_id = models.IntegerField(null=True, blank=False)
    name = models.CharField(null=True, blank=True, max_length=100)
    phone = models.CharField(null=True, blank=True, max_length=40)
    birthday = models.CharField(null=True, blank=True, max_length=100)
    balance = models.FloatField(null=True, blank=True, default=0)
    c_task = models.IntegerField(null=True, blank = True, default=0)
    date = models.DateTimeField(db_index = True, null=True, auto_now_add=True, blank=True)


class Task(models.Model):
    title = models.CharField(null=True, blank=True, max_length=200)
    url = models.CharField(null=True, blank=True, max_length=100)
    photo = models.FileField(upload_to='photos/tasks/', null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=200)
    price = models.FloatField(null=True, blank=True)
    limit = models.IntegerField(null=True, blank=True)
    done = models.IntegerField(null=True, blank=True, default=0)
    is_open = models.BooleanField(blank=True, default=True)


class Completed_task(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    task = models.IntegerField(null=True, blank=True)
    photo = models.FileField(upload_to='photos/completed_tasks/', null=True, blank=True)
    date = models.DateTimeField(db_index = True, null=True, auto_now_add=True, blank=True)
    status = models.CharField(null=True, blank=True, max_length=20, default='waiting')

class Output(models.Model): # request money
    user_id = models.IntegerField(null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=200)
    price = models.FloatField(null=True, blank=True)