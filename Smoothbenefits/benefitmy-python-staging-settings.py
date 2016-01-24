"""
Configurations for Staging/Testing environment
"""

from Smoothbenefits.base_settings import *

SITE_URL = "http://staging.workbenefits.me/"

# Logging Configurations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'key-value-pair': {
            'format': 'ID: %(cid)s; TIME: %(asctime)s; LEVEL: %(levelname)s; MESSAGE: %(message)s; PROCESS: %(process)s; THREAD: %(thread)s'
        },
    },
    'handlers': {
        'logentries_handler': {
            'token': '6fe1fb59-38a8-4b16-9448-d7bb1392ecec',
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

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbhdqcnhj8qihh',
        'USER': 'espzlrtdipscti',
        'PASSWORD': '6tw_VJkq-1pvnKAS8s0pTm540e',
        'HOST': 'ec2-54-225-101-60.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

# AMAZON AWS
## https://benefitmy.signin.aws.amazon.com
AMAZON_S3_BUCKET = 'benefitmy-staging-uploads'
AMAZON_S3_HOST = 'https://{0}.s3.amazonaws.com/'.format(AMAZON_S3_BUCKET)
AMAZON_AWS_ACCESS_KEY_ID = 'AKIAJSUUQXOJS5GNUTKA'
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
