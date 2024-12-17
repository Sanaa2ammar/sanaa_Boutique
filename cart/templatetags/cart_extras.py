# cart/templatetags/cart_extras.py

from django import template

register = template.Library()

@register.filter
def multiply(price, quantity):
    return price * quantity
