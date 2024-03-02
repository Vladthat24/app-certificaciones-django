from django import template

register = template.Library()


@register.filter
def format_number_to_money(data):
    return '{:,.2f}'.format(data)
