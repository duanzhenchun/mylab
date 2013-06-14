import os, sys
import django.core.handlers.wsgi
sys.path.append(os.path.join(os.path.dirname(__file__), 'BusD'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'BusD.settings'
application = django.core.handlers.wsgi.WSGIHandler()
