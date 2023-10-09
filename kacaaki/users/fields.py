# from django.db import models
# from django.contrib.gis.geoip2 import GeoIP2
# from user_agents import parse


# class UserAgentField(models.CharField):
#     def __init__(self, *args, **kwargs):
#         kwargs['max_length'] = 255
#         super().__init__(*args, **kwargs)

#     def pre_save(self, model_instance, add):
#         request = model_instance._request
#         user_agent = request.META.get('HTTP_USER_AGENT', '')

#         # Parse user agent string to get browser and device details
#         ua = parse(user_agent)
#         browser = ua.browser.family
#         device = ua.device.family

#         return f'{browser} ({device})'


# class UserAgentMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         request._request = request
#         response = self.get_response(request)
#         return response
