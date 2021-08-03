from django import forms
from .models import Category, News

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

import re

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=150, label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=16, label='Пароль', widget=forms.PasswordInput(attrs={'class':
                                                                                                     'form-control'}))
    password2 = forms.CharField(max_length=16, label='Подтверждение пароля:', widget=forms.PasswordInput(attrs={'class':
                                                                                                     'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# class NewsForm(forms.Form):
    # title = forms.CharField(max_length=150, label='Наименование', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # content = forms.CharField(label='Текст', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    # is_published = forms.BooleanField(label='Опубликовано', initial=True)
    # category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Выберите категорию', widget=forms.Select(attrs={'class': 'form-control'}))


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    # Кастомные валидаторы
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title
