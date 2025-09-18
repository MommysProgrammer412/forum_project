from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django import forms

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

def update_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'forum/update_post.html', {'form': form, 'post': post})

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