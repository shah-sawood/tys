from django import template

register = template.Library()

@register.filter
def convertNum2Alpha(num):
    return f"{chr(num + 96)}"
