"""
Django settings for Smoothbenefits project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_URL = "https://staging.benefitmy.com/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x_qz2d46!0dmvk9(lb_c-z%r)&_jq8nl+-_fvsywp1+j+y5oj1'

# Hash key serving as the "secret word" to help hashing
HASH_KEY = '5e14ca8a-4a48-4cf7-aa3b-e207eb1a9adb'

# Default password for initial user account setup
DEFAULT_USER_PW = 'd4gf6u0hhfg48ds321cdsf'

# Default global figure of number of minutes notification facilities should
# look back to check for user data modifications
DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES = 1440 # 24 hours

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '.benefitmy.com', 'benefitmy.com.', '.heroku.com', '.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'pipeline',
    'app',
    'emailusernames',
    'reversion',
    'django_cron',
)


AUTHENTICATION_BACKENDS = (
    'emailusernames.backends.EmailAuthBackend',
)


ENCRYPTED_FIELDS_KEYDIR = 'fieldkeys'

# Email
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'frank.qiu@gmail.com'
EMAIL_HOST_PASSWORD = 'BenefitMy2014'
EMAIL_PORT = 587
EMAIL_USE_TLS = True



MIDDLEWARE_CLASSES = (
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

CRON_CLASSES = [
    "app.scheduled_jobs.user_changes_notification.UserChangeNotifications",
]

ROOT_URLCONF = 'Smoothbenefits.urls'

WSGI_APPLICATION = 'Smoothbenefits.wsgi.application'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 20 * 60

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


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_DIRS = (
    # location of your application, should not be public web accessible
    os.path.join(os.path.join(BASE_DIR, 'app'), 'static'),
    os.path.join(BASE_DIR, 'bower_components'),
)

#Pipeline variables
PIPELINE_CSS_COMPRESSOR = ''
PIPELINE_JS_COMPRESSOR = ''


PIPELINE_CSS = {
    'home':{
        'source_filenames':(
            'stylesheets/front_end/users.css.css',
            'stylesheets/shared/variables.css.css',
            'stylesheets/shared/buttons.css.css',
            'stylesheets/shared/components.css.css',
            'stylesheets/shared/forms.css.css',
            'stylesheets/shared/global.css.css',
            'stylesheets/api.css.css',
            'stylesheets/application.css.css',
            'stylesheets/app.css',
            'stylesheets/bootstrap.css.css',
            'stylesheets/bootstrap.min.css'
            'stylesheets/framework_and_overrides.css.css',
            'stylesheets/front_end.css.css',
            'stylesheets/home.css',
            'stylesheets/layout.css',
            'stylesheets/pages.css',
            'stylesheets/users.css.css',
            'stylesheets/front_end.css.css',
            'stylesheets/application.css',
            'stylesheets/shared/devise.css.css',
            'stylesheets/shared/dashboard.css.css',
        ),
        'output_filename': 'stylesheets/home.min.css',
    },
    'dashboard':{
        'source_filenames':(
            'stylesheets/api.css.css',
            'stylesheets/application.css.css',
            'stylesheets/app.css',
            'stylesheets/bootstrap.css.css',
            'stylesheets/home.css',
            'stylesheets/layout.css',
            'stylesheets/pages.css',
            'stylesheets/users.css.css',
            'stylesheets/pixel-admin.css',
            'stylesheets/rtl.css',
            'stylesheets/themes.css',
            'stylesheets/widgets.css',
            'stylesheets/application.css',
            'stylesheets/front_end.css.css',
            'stylesheets/shared/devise.css.css',
            'stylesheets/shared/dashboard.css.css',
            'stylesheets/shared/variables.css.css',
            'stylesheets/shared/buttons.css.css',
            'stylesheets/shared/components.css.css',
            'stylesheets/shared/forms.css.css',
            'stylesheets/shared/global.css.css',
            'fonts/flaticon/flaticon.css',
        ),
        'output_filename': 'stylesheets/dashboard.min.css',
    }
}

PIPELINE_JS = {
    'home': {
        'source_filenames':(
            'js/home.js',
            'js/api.js.js',
            'js/bootstrap.min.js',
            'js/front_end/users.js.js',
            'js/google_analytics.js.js',
            'js/ie.js',
            'js/jquery.scrollspy.js',
            'js/model_factories/benefitmyDomainModelFactories.js',
            'js/services/services.js',
            'js/pixel-admin.min.js',
        ),
        'output_filename':'js/benefitmy_home.js'
    },
    'dashboard':{
        'source_filenames':(
            'js/app.js',
            'js/home.js',
            'js/api.js.js',
            'js/constants.js',
            'js/angular-multi-select.js',
            'js/application.js',
            'js/bootstrap-editable-demo.js',
            'js/bootstrap.js',
            'js/demo-mock.js',
            'js/front_end.js.js',
            'js/flashcanvas.js', 
            'js/google_analytics.js.js',
            'js/ie.js',
            'js/jquery-select2.js',
            'js/jquery-ui-extras.js',
            'js/jquery.mockjax.js',
            'js/jSignature.min.js',
            'js/users.js.js',
            'js/controllers/UserControllers.js',
            'js/controllers/BrokerControllers.js',
            'js/controllers/EmployeeControllers.js',
            'js/controllers/EmployerControllers.js',
            'js/directives/ScrollTo.js',
            'js/directives/ConfirmUnsavedOnExit.js',
            'js/directives/UploadManager.js',
            'js/directives/UploadViewer.js',
            'js/model_factories/benefitmyDomainModelFactories.js',
            'js/services/services.js',
            'js/pixel-admin.min.js',
            'js/jquery.scrollspy.js',
            'js/moment.min.js',
            'js/services/employeeBenefitElectionService.js',
            'js/services/EmployeePreDashboardValidationService.js',
            'js/services/BenefitElectionService.js',
            'js/services/CompanyEmployeeSummaryService.js',
            'js/services/DirectDepositService.js',
            'js/services/EmployeeLetterSignatureValidationService.js',
            'js/services/FsaService.js',
            'js/services/LifeInsuranceService.js',
            'js/services/benefitDisplayService.js',
            'js/services/documentTypeService.js',
            'js/services/personInfoService.js',
            'js/services/UserService.js',
            'js/services/UploadService.js',
            'js/services/employeePayrollService.js',
            'js/services/employeeProfileService.js',
            'js/services/FeatureConfigurationService.js',
            ),
        'output_filename': 'js/benefitmy.js',
    }
}
