from .base import *

DEBUG = True

CORS_ALLOW_ALL_ORIGINS = True

# Emails en consola
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Mostrar queries SQL en desarrollo
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'consola': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['consola'],
            'level': 'INFO',
        },
    },
}