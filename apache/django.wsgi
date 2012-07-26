import os
import sys

sys.path.append('/usr/local/django')
sys.path.append('/usr/local/django/youtubeinsight')
os.environ['DJANGO_SETTINGS_MODULE'] = 'youtubeinsight.production_settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
