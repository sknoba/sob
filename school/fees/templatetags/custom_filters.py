from django import template
from num2words import num2words

register = template.Library()

@register.filter
def number_to_words(value):
    """Converts a number into words"""
    if isinstance(value, (int, float)):  # Check if value is a number
        return num2words(value, lang='en_IN')  # Convert to currency words
    return value  # Return original value if it's not a number
