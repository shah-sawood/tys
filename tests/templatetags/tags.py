from django import template

register = template.Library()

@register.filter
def convertNum2Alpha(num):
    return f"{chr(num + 96)}"

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()