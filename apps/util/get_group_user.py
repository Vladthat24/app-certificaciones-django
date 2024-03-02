# Retorna si obtiene el rol asignado (Solo retorna un rol)

# 1 -> ADMINISTRADOR CREMATORIO
# 2 -> TESORERÍA
# 3 -> MESA DE PARTES
# 4 -> ADMINISTRADOR DIRIS (DSAIA)


def get_group_user(request):
    if request.user.groups.filter(name="ADMINISTRADOR CREMATORIO"):
        return 1

    if request.user.groups.filter(name="TESORERÍA"):
        return 2

    if request.user.groups.filter(name="MESA DE PARTES"):
        return 3

    if request.user.groups.filter(name="ADMINISTRADOR DIRIS"):
        return 4

    return 0
