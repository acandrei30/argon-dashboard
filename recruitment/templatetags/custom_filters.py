from django import template

register = template.Library()

@register.filter
def dict_get(dictionary, key):
    """Retrieve a value from a dictionary using a key."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, "")
    return ""
