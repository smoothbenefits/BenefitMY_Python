"""
Configurations for Beta environment
"""
import logging
from logentries import LogentriesHandler
from Smoothbenefits.base_settings import *

# Environment Identification
IS_PRODUCTION_ENVIRONMENT = True

SITE_URL = "https://app.workbenefits.me/"

# Time Tracking Service URL
TIME_TRACKING_SERVICE_URL = "https://timetracking.workbenefits.me/"

# Certificate of Insurance Service URL
COI_SERVICE_URL = "https://insurcert.workbenefits.me/"

ENVIRONMENT_IDENTIFIER = 'production'

# Logging Configurations
LOGGING['handlers']['logentries_handler']['token'] = '11a32264-c904-4765-96c0-fe6e7fbdb09c'

# Default global figure of number of minutes notification facilities should
# look back to check for user data modifications
DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES = 1440 # 24 hours

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

# Application configurations
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cid.middleware.CidMiddleware',
    'app.middlewares.hash_pk_validation_middleware.HashPkValidationMiddleware',
    'app.middlewares.logging_middleware.LoggingMiddleware',
    'app.middlewares.cors_middleware.CorsMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'de94t1pirsgrs2',
        'USER': 'ub3su5lfgiceuv',
        'PASSWORD': 'p7p9qibvs0en4naevs5abar79t2',
        'HOST': 'ec2-52-5-245-203.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

# AMAZON AWS
## https://benefitmy.signin.aws.amazon.com
AMAZON_S3_BUCKET = 'benefitmy-beta1-uploads'
AMAZON_S3_HOST = 'https://{0}.s3.amazonaws.com/'.format(AMAZON_S3_BUCKET)
AMAZON_AWS_ACCESS_KEY_ID = 'AKIAIYFT3OPIYKIGCTZA'
AMAZON_AWS_SECRET = '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'
AMAZON_S3_UPLOAD_POLICY= {
    "conditions": [
        {"bucket": AMAZON_S3_BUCKET},
        ["starts-with", "$key", ""],
        {"acl": "private"},
        ["starts-with", "$Content-Type", ""],
        ["starts-with", "$filename", ""],
        ["content-length-range", 0, 52428800],
        {"x-amz-server-side-encryption": "AES256"},
    ]
}
