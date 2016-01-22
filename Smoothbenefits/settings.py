"""
Configurations for local environment
"""
import logging
from logentries import LogentriesHandler
from Smoothbenefits.base_settings import *

SITE_URL = "https://localhost:8000/"

# Logging Configurations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'key-value-pair': {
            'format': 'ID: %(cid)s; TIME: %(asctime)s; LEVEL: %(levelname)s; MESSAGE: %(message)s;'
        },
    },
    'handlers': {
        'logentries_handler': {
            'token': '980781a6-72cf-4dd7-b6ae-57fc3e7d7262',
            'class': 'logentries.LogentriesHandler',
            'formatter': 'key-value-pair'
        },
    },
    'filters': {
        'correlation': {
            (): 'cid.log.CidContextFilter'
        },
    },
    'loggers': {
        'logentries': {
            'handlers': ['logentries_handler'],
            'level': 'INFO',
            'propagate':True,
            'filters': ['correlation']
        },
    },
}

# Default global figure of number of minutes notification facilities should
# look back to check for user data modifications
DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES = 1440 # 24 hours

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

PDFTK_BIN = '/usr/bin/pdftk'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Benefits_DB',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# AMAZON AWS
## https://benefitmy.signin.aws.amazon.com
AMAZON_S3_BUCKET = 'benefitmy-dev-uploads'
AMAZON_S3_HOST = 'https://{0}.s3.amazonaws.com/'.format(AMAZON_S3_BUCKET)
AMAZON_AWS_ACCESS_KEY_ID = 'AKIAIZJ3E4NCV33WGQ5Q'
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
