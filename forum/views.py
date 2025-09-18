from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

def index(request):
    posts = Post.objects.all() 
    return render(request, 'forum/index.html', {'posts': posts})

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Перенаправление на главную страницу
    else:
        form = PostForm()
    return render(request, 'forum/add_post.html', {'form': form})