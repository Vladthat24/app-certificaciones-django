# from setup.models.menu import Menu
#
#
# def update_menu(request):
#     try:
#         request.session['menu_children'] = Menu.objects.get(pk=request.GET.get('children_id')).id
#         request.session['menu_parent'] = Menu.objects.get(pk=request.GET.get('children_id')).parent.id
#     except Menu.DoesNotExist:
#         pass
