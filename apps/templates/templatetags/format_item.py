# # coding=utf-8
# from django import template
#
# from apps.reclamo.models.entidad_reclamo import MESES
#
# register = template.Library()
#
#
# @register.filter
# def get_item(dictionary, key):
#     return dictionary.get(key)
#
#
# @register.filter
# def filter_mes(value):
#     res = [tup for tup in MESES if (tup[0] == value)]
#     return res[0][1]
