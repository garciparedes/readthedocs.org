"""Docker deployment settings, including local_settings, if present."""
from __future__ import absolute_import

import os

from .base import CommunityBaseSettings


class CommunityDockerSettings(CommunityBaseSettings):
    """Settings for Docker deployment"""

    PRODUCTION_DOMAIN = os.getenv('PRODUCTION_DOMAIN', 'localhost:8000')
    WEBSOCKET_HOST = os.getenv('PRODUCTION_DOMAIN', 'localhost:8088')

    @property
    def DATABASES(self):  # noqa
        return {
            # 'default': {
            #     'ENGINE': 'django.db.backends.mysql',
            #     'NAME': 'db',
            #     'USER': 'dbuser',
            #     'PASSWORD': 'dbpw',
            #     'HOST': 'mysql',
            #     'PORT': '3306',
            #     'TEST': {
            #         'NAME': 'db_test',
            #     },
            # }
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(self.SITE_ROOT, 'dev.db'),
            }
        }

    DONT_HIT_DB = False

    ACCOUNT_EMAIL_VERIFICATION = 'none'
    SESSION_COOKIE_DOMAIN = None
    CACHE_BACKEND = 'dummy://'

    SLUMBER_USERNAME = 'docker'
    SLUMBER_PASSWORD = 'docker'  # noqa: ignore dodgy check
    SLUMBER_API_HOST = os.getenv('SLUMBER_API_HOST', "http://" + PRODUCTION_DOMAIN)

    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ALWAYS_EAGER = True
    CELERY_TASK_IGNORE_RESULT = False

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    FILE_SYNCER = 'readthedocs.builds.syncers.LocalSyncer'

    CORS_ORIGIN_WHITELIST = (
        'localhost:8000',
    )

    # Disable auto syncing elasticsearch documents in development
    ELASTICSEARCH_DSL_AUTOSYNC = True

    ALLOW_PRIVATE_REPOS = True

    @property
    def LOGGING(self):  # noqa - avoid pep8 N802
        logging = super().LOGGING
        logging['formatters']['default']['format'] = '[%(asctime)s] ' + self.LOG_FORMAT
        # Allow Sphinx and other tools to create loggers
        logging['disable_existing_loggers'] = False
        return logging


CommunityDockerSettings.load_settings(__name__)
