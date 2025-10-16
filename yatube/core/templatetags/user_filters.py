from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    try:
        return field.as_widget(attrs={'class': css})
    except AttributeError:
        return field  

@register.filter
def addplaceholder(field, placeholder):
    return field.as_widget(attrs={'placeholder': placeholder})
