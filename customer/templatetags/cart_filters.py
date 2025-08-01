# In filters.py
from django import template

register = template.Library()

@register.filter
def total_price(cart_items):
    return sum(item['product'].price * item['quantity'] for item in cart_items)


@register.filter
def multiply(value, arg):
    return value * arg
