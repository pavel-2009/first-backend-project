from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Post, Group
from .forms import PostForm


def index(request):
    posts = Post.objects.select_related('author', 'group')\
        .all().order_by('-pub_date')

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')

    page = paginator.get_page(page_number)

    context = {
        'page_obj': page,
    }

    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug.lower())

    posts = Post.objects.select_related('author', 'group')\
        .filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')

    page = paginator.get_page(page_number)

    text = "Здесь будет информация о группах проекта Yatube"
    context = {
        'text': text,
        'group': group,
        'page_obj': page,
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    posts = Post.objects.select_related('author', 'group')\
        .filter(author__username=username).order_by('-pub_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page_obj': page,
        'username': username,
        'posts': posts,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required(redirect_field_name='next', login_url='users:login')
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user.username)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required(redirect_field_name='next', login_url='users:login')
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if post.author != user:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()

        return redirect('posts:post_detail', post_id=post_id)

    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)
