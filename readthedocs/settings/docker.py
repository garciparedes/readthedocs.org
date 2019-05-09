"""Docker deployment settings, including local_settings, if present."""
from __future__ import absolute_import

import os

from .base import CommunityBaseSettings


class CommunityDockerSettings(CommunityBaseSettings):
    """Settings for Docker deployment"""

    PRODUCTION_DOMAIN = '{}:{}'.format(os.getenv('DOMAIN'), os.getenv('PORT'))
    WEBSOCKET_HOST = '{}:8088'.format(os.getenv('DOMAIN'))

    @property
    def DATABASES(self):  # noqa
        return {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': '{}_db'.format(os.getenv('PROJECT_NAME')),
                'USER': os.getenv('PROJECT_NAME'),
                'PASSWORD': os.getenv('MYSQL_PASSWORD'),
                'HOST': 'mysql',
                'PORT': '3306',
                'TEST': {
                    'NAME': 'db_test',
                },
            },
            # 'default': {
            #     'ENGINE': 'django.db.backends.sqlite3',
            #     'NAME': os.path.join(self.SITE_ROOT, 'dev.db'),
            # }
        }

    DONT_HIT_DB = False

    ACCOUNT_EMAIL_VERIFICATION = 'none'
    SESSION_COOKIE_DOMAIN = None
    CACHE_BACKEND = 'dummy://'

    SLUMBER_USERNAME = 'test'
    SLUMBER_PASSWORD = 'test'  # noqa: ignore dodgy check
    SLUMBER_API_HOST = 'http://127.0.0.1:8000'
    PUBLIC_API_URL = 'http://127.0.0.1:8000'

    BROKER_URL = 'redis://{}:6379/0'.format(os.getenv('DOMAIN'))
    CELERY_RESULT_BACKEND = 'redis://{}:6379/0'.format(os.getenv('DOMAIN'))
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ALWAYS_EAGER = True
    CELERY_TASK_IGNORE_RESULT = False

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    FILE_SYNCER = 'readthedocs.builds.syncers.LocalSyncer'

    # For testing locally. Put this in your /etc/hosts:
    # 127.0.0.1 test
    # and navigate to http://test:8000
    CORS_ORIGIN_WHITELIST = (
        'test:8000',
    )

    # Disable auto syncing elasticsearch documents in development
    ELASTICSEARCH_DSL_AUTOSYNC = False

    @property
    def LOGGING(self):  # noqa - avoid pep8 N802
        logging = super().LOGGING
        logging['formatters']['default']['format'] = '[%(asctime)s] ' + self.LOG_FORMAT
        # Allow Sphinx and other tools to create loggers
        logging['disable_existing_loggers'] = False
        return logging

    @property
    def INSTALLED_APPS(self):
        apps = super().INSTALLED_APPS
        apps.append('debug_toolbar')
        return apps

    @property
    def MIDDLEWARE(self):
        middlewares = list(super().MIDDLEWARE)
        middlewares.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
        return middlewares



CommunityDockerSettings.load_settings(__name__)
