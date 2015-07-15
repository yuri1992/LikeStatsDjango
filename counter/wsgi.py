"""
WSGI config for counter project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
<<<<<<< HEAD
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
=======

import os
>>>>>>> bdc7b87baa7c871d8ddc960065d07edba733ddc0
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "counter.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
