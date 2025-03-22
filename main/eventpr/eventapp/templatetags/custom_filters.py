from django import template
import json

register = template.Library()

@register.filter
def endswith(value, arg):
    """Returns True if the value ends with the given argument."""
    return value.endswith(arg)

@register.filter
def jsonify(value):
    return json.dumps(value)


@register.filter
def get_addon_by_name(customization_options, addon_name):
    """Get the addon from customization options by its name."""
    if not customization_options:
        return None
    return next((addon for addon in customization_options if addon['name'] == addon_name), None)

@register.filter
def get_item(dictionary, key):
    """Returns the value of the given key in a dictionary."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, "")
    return ""