"""
Configuations for Demo environment
"""
from Smoothbenefits.base_settings import *

SITE_URL = "http://demo.workbenefits.me/"

# Logging Configurations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'key-value-pair': {
            'format': 'TIME: %(asctime)s; LEVEL: %(levelname)s; REPORTER: %(module)s, MESSAGE: %(message)s; '
        },
    },
    'handlers': {
        'logentries_handler': {
            'token': 'cc97e28c-6b76-4466-bd5b-f260ea68cf4b',
            'class': 'logentries.LogentriesHandler',
            'formatter': 'key-value-pair'
        },
    },
    'loggers': {
        'logentries': {
            'handlers': ['logentries_handler'],
            'level': 'INFO',
            'propagate':True,
        },
    },
}

# Default global figure of number of minutes notification facilities should
# look back to check for user data modifications
DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES = 1440 # 24 hours

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

# Application definition
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
    'app.middlewares.hash_pk_validation_middleware.HashPkValidationMiddleware',
    'reversion.middleware.RevisionMiddleware',
)


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dcv4d46p3t7lkj',
        'USER': 'feblksfyqbhdjv',
        'PASSWORD': '7F2Flb6iVg-jGTtD2dsoWXzKi3',
        'HOST': 'ec2-54-225-101-202.compute-1.amazonaws.com',
        'PORT': '5432',
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
