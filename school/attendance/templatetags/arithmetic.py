from django import template

register = template.Library()

@register.filter
def add(value, arg):
    """Adds two values."""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return 0

@register.simple_tag
def calculate_absent(total_students, present_boy, present_girl):
    try:
        present_total = int(present_boy) + int(present_girl)
        return int(total_students) - present_total
    except (ValueError, TypeError):
        return total_students
        