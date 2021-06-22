from django import template
from datetime import datetime
import pytz, locale

register = template.Library()

@register.filter
def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)

@register.filter
def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)

@register.filter
def div(value, arg):
    "Divides the value by the arg"
    return int(value) / int(arg)

@register.filter
def dt_to_ro(value):
    "Converts datetime to local timezone"
    locale.setlocale(locale.LC_TIME, "ro_RO")
    tz = pytz.timezone('Europe/Bucharest')
    if value:
        return value.astimezone(tz).strftime("%d %b %Y %H:%M")
    else: 
        return value

@register.filter
def as_range(value):
    "Generates range from 0 to the value inputted"
    return list(range(value))

@register.filter
def key(d, key_name):
    # try:
    #     # make sure if you pass an int it stays an int as jinja may convert it
    #     key_name = int(key_name)
    # except ValueError:
    #     # key is a string
    #     pass
    return d[key_name]

# # Alternative filter register code
# template.register_filter('mult', mult, True)
# template.register_filter('sub', sub, True)
# template.register_filter('div', div, True)