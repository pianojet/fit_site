"""
WSGI config for fit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fit.settings.dev')  # Default value

class EnvironMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'DJANGO_SETTINGS_MODULE' in environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = environ['DJANGO_SETTINGS_MODULE']
        return self.app(environ, start_response)


from django.core.wsgi import get_wsgi_application

application = EnvironMiddleware(get_wsgi_application())
