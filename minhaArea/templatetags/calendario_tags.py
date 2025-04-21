from django import template
import calendar
from datetime import date

register = template.Library()

@register.simple_tag
def get_month_days(year, month):
    # Retorna uma lista de tuplas com (número do dia, nome do dia)
    num_days = calendar.monthrange(year, month)[1]
    first_day = date(year, month, 1)
    days = [(day, calendar.day_name[date(year, month, day).weekday()]) for day in range(1, num_days + 1)]
    return days

@register.simple_tag
def get_month_name(month):
    return calendar.month_name[month]

@register.filter
def dict_get(dictionary, key):
    return dictionary.get(key)

@register.filter
def to_range(start, end):
    return range(start, end)

@register.filter
def get_month_days(month, year):
    return range(1, calendar.monthrange(year, month)[1] + 1)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])

@register.simple_tag
def get_month_name(month_number):
    return calendar.month_name[month_number]
