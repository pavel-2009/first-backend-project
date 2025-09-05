from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post, Group, User

from datetime import datetime


def index(request):
    keyword = request.GET.get("q", None)
    if keyword:
        posts = Post.objects.filter(text__contains=keyword).select_related('author').select_related('group')
    else:
        posts = None

    return render(request, "posts/index.html", {"posts": posts, "keyword": keyword})


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

