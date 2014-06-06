"""
WSGI config for mmcrp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('/Users/narobert/mmcrp/mmcrp/mmcrp/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmcrp.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
