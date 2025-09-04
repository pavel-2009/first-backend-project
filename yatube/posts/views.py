from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post, Group


def index(request):
    text = 'Это главная страница проекта Yatube.'
    context = {
        'text': text,
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    text = "Здесь будет информация о группах проекта Yatube"
    context = {
        'text': text,
        'posts': posts,
        'group': group,
    }

    return render(request, 'posts/group_list.html', context)

