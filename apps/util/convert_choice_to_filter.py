def convert_choice_to_filter(choice):
    choice_new = ()
    for i in choice:
        choice_new += ((str(i[0]), i[1]),)
    return choice_new
