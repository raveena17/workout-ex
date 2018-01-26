# from django.conf import settings
# from django.contrib.sites.models import Site

# def get_full_domain():
#     scheme = 'https'
#     if not settings.SECURE_SSL_REDIRECT:
#         scheme = 'http'
#     return '%s://%s' % (scheme, Site.objects.get_current().domain)


from django.conf import settings
from django.contrib.sites.models import Site
import socket
import sys

def get_full_domain():
	# import pdb;pdb.set_trace()
	host = socket.gethostname()

	scheme = 'https'
	if not settings.SECURE_SSL_REDIRECT:
	    scheme = 'http'
	# return '%s://%s' % (scheme, Site.objects.get_current().domain)
	return '%s://%s' % (scheme, sys.argv[-1])

# def get_full_domain():
#     scheme = 'https'
#     if not settings.SECURE_SSL_REDIRECT:
#         scheme = 'http'
#     return '%s://%s' % (scheme, Site.objects.get_current().domain)