from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.group_posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        'page_obj': page_obj,
    }
    return render(request, "posts/group_list.html", context)


def search(request):
    keyword = request.GET.get("search", None)
    if keyword:
        posts = Post.objects.select_related(
            'author'
        ).select_related(
            'group'
        ).filter(
            text__contains=keyword
        )
    else:
        posts = None
    context = {
        "posts": posts,
        "keyword": keyword,
    }
    return render(request, "posts/index.html", context=context)
    # TODO Поломался поиск, надо разобраться как его пофиксать :)
    #  Поломался из-за пагинации.


def profile(request, username):
    # получить список постов отфильтрованному по имени пользователя - username.
    author = get_object_or_404(User, username=username)
    post_list = author.user_posts.all()
    count = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "username": username,
        "count": count,
        "author": author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    count = post.author.user_posts.count()
    context = {
        "post": post,
        "count": count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user)
    context = {
        "form": form,
    }
    return render(request, "posts/create_post.html", context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post.save()
            return redirect('posts:post_detail', post_id)
        context = {
            "form": form,
        }
        return render(request, "posts/create_post.html", context)
    return redirect('posts:post_detail', post_id)
