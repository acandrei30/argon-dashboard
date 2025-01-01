from django import template
from datetime import datetime

register = template.Library()  # Declare register only once.

@register.filter
def dict_get(dictionary, key):
    """Retrieve a value from a dictionary using a key."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, "")
    return ""

@register.filter
def date_diff(date1, date2):
    """
    Calculate the difference in days between two dates.
    """
    try:
        if date1 and date2:
            delta = (datetime.strptime(str(date1), "%Y-%m-%d") - 
                     datetime.strptime(str(date2), "%Y-%m-%d"))
            return delta.days
    except (ValueError, TypeError):
        pass  # Handle invalid date formats gracefully
    return None

@register.filter
def abs_value(value):
    """
    Returns the absolute value of a number.
    """
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        return value
