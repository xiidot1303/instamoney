from django.forms import ModelForm, widgets
from app.models import *
from django import forms


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = {'title', 'url', 'photo', 'description', 'price', 'limit'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}), 
            'price': forms.TextInput(attrs={'class': 'form-control'}), 
            'limit': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Названия',
            'url': 'Ссылка', 
            'photo': 'Фото', 
            'description': 'Описания', 
            'price': 'Цена', 
            'limit': 'Лимит'
            
        }
    field_order = ['title', 'url', 'photo', 'description', 'price', 'limit']


class SendmessageForm(forms.Form):
    select = forms.CharField(max_length=50, label='Ползователь', widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-control'}))
    photo = forms.FileField(label='Фото', localize=True, required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
    field_order = ['select', 'message', 'photo']

    # labels = {
    #     'select': 'Ползователь',
    #     'message': 'Сообщение',
    #     'photo': 'Фото',
    # }

