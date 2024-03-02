def get_referer(request):
    referer = ""
    if request.META.get('HTTP_REFERER'):
        if len(request.META.get('HTTP_REFERER').split("?")) > 1:
            referer = "?" + request.META.get('HTTP_REFERER').split("?")[-1]

    if len(request.get_full_path().split("?")) > 1:
        referer = "?" + request.get_full_path().split("?")[-1]

    return referer
