def get_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip :
        ip = ip.split(',')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip