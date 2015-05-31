"""
Configurations for Beta Plus environment
"""
from Smoothbenefits.base_settings import *

SITE_URL = "https://beta.benefitmy.com/"

# Default global figure of number of minutes notification facilities should
# look back to check for user data modifications
DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES = 1440 # 24 hours

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

# Application configurations
# comment out SSL settings for now.
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# MIDDLEWARE_CLASSES = (
#     'sslify.middleware.SSLifyMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'app.middlewares.hash_pk_validation_middleware.HashPkValidationMiddleware',
#     'reversion.middleware.RevisionMiddleware',
# )


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd2iunbdrtrefd1',
        'USER': 'hgnlizdwiywcty',
        'PASSWORD': '85TC_pb4T03A7HMUmV7YGOrp-h',
        'HOST': 'ec2-54-243-187-196.compute-1.amazonaws.com',
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
