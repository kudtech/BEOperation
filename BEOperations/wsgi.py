"""
WSGI config for BEOperations project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
# import socketio
# from socketio_app.views import sio
# from django.core.wsgi import get_wsgi_application
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BEOperations.settings')
application = get_wsgi_application()

# application = socketio.WSGIApp(sio ,application)