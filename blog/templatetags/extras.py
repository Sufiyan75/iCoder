from django import template

register = template.Library()

@register.filter(name='get_val')
def get_val(dict, key):
    return dict.get(key)

@register.filter(name='upto')
def upto(value):
    return range(1, value + 1)