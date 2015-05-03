"""
Configurations for Sandbox environment
"""

from Smoothbenefits.base_settings import *

SITE_URL = "http://sandbox.benefitmy.com/"

# Default global figure of number of minutes notification facilities should
# look back to check for user data modifications
DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES = 1440 # 24 hours

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Session expiration settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 20 * 60

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd68sd5k6b9j9hk',
        'USER': 'byqrksqolpdafr',
        'PASSWORD': 'yi9gkFL5Dco8T5dXqeO9di5UHd',
        'HOST': 'ec2-54-163-226-9.compute-1.amazonaws.com',
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