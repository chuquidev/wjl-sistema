from .base import *

DEBUG = False

CORS_ALLOWED_ORIGINS = config('CORS_ORIGINS', default='').split(',')

# Seguridad HTTPS
SECURE_SSL_REDIRECT             = True
SECURE_HSTS_SECONDS             = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_PRELOAD             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_BROWSER_XSS_FILTER       = True
SECURE_CONTENT_TYPE_NOSNIFF     = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# Emails reales
EMAIL_BACKEND  = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST     = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT     = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS  = True
EMAIL_HOST_USER     = config('EMAIL_USUARIO', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_CONTRASENA', default='')