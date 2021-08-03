from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import News, Category
from .forms import *
from .utils import *

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрировались!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserRegisterForm()
        context = {'form': form}
    return render(request, 'news/register.html', context=context)

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно залогинились!')
            return redirect('home')
        else:
            messages.error(request, 'Не вверный ввод пользователя или пароля!')
    else:
        form = UserLoginForm()
        context = {'form': form}
    return render(request, 'news/login.html', context=context)

def user_logout(request):
    logout(request)
    return redirect('login')

def test(request):
    objects = ['Kristina', 'Timur', 'Anastasia']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page')
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})


class HomeNews(MyMixin, ListView):

    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    extra_context = {'title': 'Главная'}
    mixin_prop = 'hello world'
    paginate_by = 2
    # queryset = News.objects.select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):

    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):

    model = News
    pk_url_kwarg = 'news_id'
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):

    form_class = NewsForm
    template_name = 'news/add_news.html'

    # For check auth: redirect or get error
    # login_url = '/admin/'
    raise_exception = True

    # For redirect
    # success_url = reverse_lazy('home')


# def index(request):
#     news = News.objects.all()
#     # res = '<h1>New\'s list</h1>'
#     # for item in news:
#     #     res += f'<div>\n<h2>{item.title}</h2>\n<p>{item.content}<p>\n</div>\n<hr>'
#
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#
#     return render(request, template_name='news/index.html', context=context)

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news': news,
#         'category': category
#     }
#     return render(request, template_name='news/category.html', context=context)

# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     context = {
#         'news_item': news_item,
#     }
#     return render(request=request, template_name='news/view_news.html', context=context)

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # title = form.cleaned_data['title']
#             # News.object.create(title=title)
#             #news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     context = {
#         'form': form,
#     }
#     return render(request=request, template_name='news/add_news.html', context=context)