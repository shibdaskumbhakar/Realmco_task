from django import template

register = template.Library()


@register.simple_tag
def multiply(a, b):
    return a*b


@register.filter
def cal_total_amount(cart):
    total = 0
    for c in cart:
        price = c.get('item').price
        quentity = c.get('quentity')
        single_item_price = multiply(quentity, price)
        total = total + single_item_price
    return total
