from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "₹ "+str(number)

@register.filter(name='multiply')
def multiply(quantity,price):
    try:
        return quantity * price
    except (TypeError, ValueError):
        return 0