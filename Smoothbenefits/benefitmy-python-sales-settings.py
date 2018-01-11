"""
Configuations for Sales/demo2 environment
"""
from Smoothbenefits.base_settings import *

SITE_URL = "http://demo2.workbenefits.me/"

# Time Tracking Service URL
TIME_TRACKING_SERVICE_URL = "http://stage.timetracking.workbenefits.me/"

# Certificate of Insurance Service URL
COI_SERVICE_URL = "http://stage.insurcert.workbenefits.me/"

ENVIRONMENT_IDENTIFIER = 'demo2'

# Logging Configurations
LOGGING['handlers']['logentries_handler']['token'] = '4b8f49e5-3387-4ed4-8393-c28b9edaf6a7'

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
        'NAME': 'd45o602gtuai7',
        'USER': 'gdydygikyhlwiq',
        'PASSWORD': 'moRMX-g_xak1u2jPTno-oS-82N',
        'HOST': 'ec2-23-21-193-140.compute-1.amazonaws.com',
        'PORT': '5432',
        'CONN_MAX_AGE': 60
    }
}

# AMAZON AWS
## https://benefitmy.signin.aws.amazon.com
AMAZON_S3_BUCKET = 'benefitmy-demo2-uploads'
AMAZON_S3_HOST = 'https://{0}.s3.amazonaws.com/'.format(AMAZON_S3_BUCKET)
AMAZON_AWS_ACCESS_KEY_ID = 'AKIAIGNPTZDEZGOOII4A'
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
