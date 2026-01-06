import os
import sys

path = '/home/georgequao/BE_capstone_project/budget_tracker'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'budget_tracker.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()