from django.urls import path
from .views import AboutAuthorView, TechView

app_name = 'about'

urlpatterns = [
    path('author/', AboutAuthorView.as_view(), name='author'),
    path('tech/', TechView.as_view(), name='tech'),   
]

