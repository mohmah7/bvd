import os
import sys

import site
site.addsitedir('/home/django/.virtualenvs/bvd/lib/python2.7/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'bvd.settings'
sys.path.append('/opt/bvd/src')
sys.path.append('/opt/bvd/src/bvd')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()