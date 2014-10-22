from __future__ import unicode_literals

import os
import sys
import site



# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/jacko/.venv/skillup/local/lib/python2.7/site-packages')

print sys.path
path = '/home/jacko/Projects'
if path not in sys.path:
    sys.path.append(path)

import payments


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
settings_module = "%s.settings" % PROJECT_ROOT.split(os.sep)[-1]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
  