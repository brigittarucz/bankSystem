from django.core.exceptions import PermissionDenied
from django.conf import settings


class IPFilterMiddleware:

   def __init__(self, get_response):
      self.get_response = get_response
      # One-time configuration and initialization.

   def __call__(self, request):
    
      allowed_ip_addresses = '127.0.0.2'
      private_paths = settings.PRIVATE_PATHS['ONLY_FOR_EMPLOYEES']
      employee_ip = request.META.get('REMOTE_ADDR')
      requested_path = request.path
      print(f'** client ip address: {employee_ip}')
      if employee_ip != allowed_ip_addresses and requested_path in private_paths:
         raise PermissionDenied()
         print('cannot continue')


      response = self.get_response(request)

      # Code to be executed for each request/response after
      # the view is called.

      response['X-IP-FILTER'] = 'IP Filter for employees - Banking System'

      return response