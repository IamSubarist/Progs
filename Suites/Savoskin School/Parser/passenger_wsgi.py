# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/s/savsch2z/savsch2z.beget.tech/MBOU')
sys.path.insert(1, '/home/s/savsch2z/savsch2z.beget.tech/venv_django/lib/python3.8/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'MBOU.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()