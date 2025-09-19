from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, UserRegisterForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView
from django.contrib.auth import login

def index(request):
    posts = Post.objects.all() 
    return render(request, 'forum/index.html', {'posts': posts})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Устанавливаем автора
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'forum/add_post.html', {'form': form})

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)
    return render(request, 'forum/update_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('index')  # Перенаправление на страницу со списком постов

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = UserRegisterForm()
    return render(request, 'forum/register.html', {'form': form})

@login_required
def user_posts(request, user_id):
    posts = Post.objects.filter(author_id=user_id)
    return render(request, 'forum/user_posts.html', {'posts': posts})

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)  # Вход пользователя
        return super().form_valid(form)