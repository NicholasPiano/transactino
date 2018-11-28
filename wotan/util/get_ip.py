
def get_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for is not None:
    return x_forwarded_for.split(',')[0]

  return request.META.get('REMOTE_ADDR')
