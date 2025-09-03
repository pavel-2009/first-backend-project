from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    text = 'Это главная страница проекта Yatube.'
    context = {
        'text': text,
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    slug = slug
    text = "Здесь будет информация о группах проекта Yatube"
    context = {
        'slug': slug,
        'text': text,
    }

    return render(request, 'posts/group_list.html', context)

