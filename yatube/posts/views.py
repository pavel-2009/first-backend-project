from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from .models import Post, Group


def index(request):
    posts = Post.objects.all().order_by('-pub_date')

    paginator = Paginator(posts, 10) 

    page_number = request.GET.get('page')   

    page = paginator.get_page(page_number)

    context = {
        'page_obj': page,
    }

    return render(request, "posts/index.html", context)


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

