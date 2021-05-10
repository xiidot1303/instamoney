from django.forms import ModelForm
from app.models import *
from django import forms


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = {'url', 'photo', 'description', 'price', 'limit'}
        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}), 
            'price': forms.TextInput(attrs={'class': 'form-control'}), 
            'limit': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'url': 'Ссылка', 
            'photo': 'Фото', 
            'description': 'Описания', 
            'price': 'Цена', 
            'limit': 'Лимит'
            
        }
    field_order = ['url', 'photo', 'description', 'price', 'limit']