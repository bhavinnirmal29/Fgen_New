from django import template

register = template.Library()

@register.filter
def trim_path(value):
    # Ensure the value is a string
    value = str(value)
    
    # Handle media files (new path)
    if '/media/' in value:
        return value
    
    # Handle static files (legacy path)
    index = value.find('/static/')
    if index != -1:
        return value[index:]
    
    return value