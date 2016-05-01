"""
Configurations for local environment
"""
import logging
from logentries import LogentriesHandler
from Smoothbenefits.base_settings import *

SITE_URL = "http://localhost:8000/"

# Time Tracking Service URL
TIME_TRACKING_SERVICE_URL = 'http://localhost:6999/'

# Certificate of Insurance Service URL
COI_SERVICE_URL = "http://localhost:10999/"

ENVIRONMENT_IDENTIFIER = 'localhost'

# Logging Configurations
LOGGING['handlers']['logentries_handler']['token'] = '980781a6-72cf-4dd7-b6ae-57fc3e7d7262'

# Default global figure of number of minutes notification facilities should
# look back to check for user data modifications
DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES = 1440 # 24 hours

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOG_TO_CONSOLE = True

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
