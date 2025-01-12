from django import template

register = template.Library()

@register.filter
def percentage(score, max_points):
    try:
        return (int(score) / int(max_points)) * 100
    except (ValueError, ZeroDivisionError):
        return 0
