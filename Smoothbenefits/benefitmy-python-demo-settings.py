"""
Configuations for Demo environment
"""
from Smoothbenefits.base_settings import *

SITE_URL = "http://demo.workbenefits.me/"

# Time Tracking Service URL
TIME_TRACKING_SERVICE_URL = "http://stage.timetracking.workbenefits.me/"

# Certificate of Insurance Service URL
COI_SERVICE_URL = "http://stage.insurcert.workbenefits.me/"

ENVIRONMENT_IDENTIFIER = 'demo'

# Logging Configurations
LOGGING['handlers']['logentries_handler']['token'] = 'cc97e28c-6b76-4466-bd5b-f260ea68cf4b'

# Default global figure of number of minutes notification facilities should
# look back to check for user data modifications
DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES = 1440 # 24 hours

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dadsss51kovk6l',
        'USER': 'epkcctcekxsjov',
        'PASSWORD': '57869fdff3f5e956f1dd915eda02b64c0adc956f8ab15b12b6629c60e6b6b79e',
        'HOST': 'ec2-54-221-241-23.compute-1.amazonaws.com',
        'PORT': '5432',
        'CONN_MAX_AGE': 60
    }
}

# AMAZON AWS
## https://benefitmy.signin.aws.amazon.com
AMAZON_S3_BUCKET = 'benefitmy-demo-uploads'
AMAZON_S3_HOST = 'https://{0}.s3.amazonaws.com/'.format(AMAZON_S3_BUCKET)
AMAZON_AWS_ACCESS_KEY_ID = 'AKIAI2LOIPXMEPLCJBEA'
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
