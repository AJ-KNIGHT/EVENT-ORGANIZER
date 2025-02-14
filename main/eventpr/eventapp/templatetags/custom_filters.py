from django import template

register = template.Library()

@register.filter
def endswith(value, arg):
    """Returns True if the value ends with the given argument."""
    return value.endswith(arg)
