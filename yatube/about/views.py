from django.views.generic import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

class TechView(TemplateView):
    template_name = 'about/tech.html'
