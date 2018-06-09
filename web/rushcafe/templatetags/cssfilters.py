from django import template
from django.utils.safestring import SafeText

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    print(value)
    print(type(value))
    return value.as_widget(attrs={'class': arg})