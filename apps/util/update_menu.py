from setup.models.menu import Menu


def update_menu(request):
    try:
        request.session['menu_children'] = Menu.objects.get(pk=request.GET.get('children_id')).id
        request.session['menu_children_name'] = Menu.objects.get(pk=request.GET.get('children_id')).name
        request.session['menu_parent'] = Menu.objects.get(pk=request.GET.get('children_id')).parent.id
        request.session['menu_parent_name'] = Menu.objects.get(pk=request.GET.get('children_id')).parent.name
    except Menu.DoesNotExist:
        pass
