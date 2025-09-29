from django import template

register = template.Library()

@register.filter
def addclass(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter
def max_length(text, length):
    if len(text) > length:
        return text[:length] + "..."
    return text