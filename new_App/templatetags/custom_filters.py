from django import template

register = template.Library()

@register.filter
def trim_path(value):
    # Ensure the value is a string
    value = str(value)
    # Find the first occurrence of '/static/' and return the substring starting from there
    index = value.find('/static/')
    if index != -1:
        return value[index:]
    return value