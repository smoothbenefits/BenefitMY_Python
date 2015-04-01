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

SITE_URL = "https://beta.benefitmy.com/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x_qz2d46!0dmvk9(lb_c-z%r)&_jq8nl+-_fvsywp1+j+y5oj1'

# Hash key serving as the "secret word" to help hashing
HASH_KEY = '5e14ca8a-4a48-4cf7-aa3b-e207eb1a9adb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

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
)

ROOT_URLCONF = 'Smoothbenefits.urls'

WSGI_APPLICATION = 'Smoothbenefits.wsgi.application'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 5 * 60

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd1ac9dq1g23jd6',
        'USER': 'phvrvgtybibihz',
        'PASSWORD': 'seOe5bLgAF83xQpxUMy8ck4VL8',
        'HOST': 'ec2-54-235-127-33.compute-1.amazonaws.com',
        'PORT': '5432',
    }
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
            'js/google_analytics.js.js',
            'js/ie.js',
            'js/jquery-select2.js',
            'js/jquery-ui-extras.js',
            'js/jquery.mockjax.js',
            'js/users.js.js',
            'js/controllers/UserControllers.js',
            'js/controllers/BrokerControllers.js',
            'js/controllers/EmployeeControllers.js',
            'js/controllers/EmployerControllers.js',
            'js/directives/ScrollTo.js',
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
            ),
        'output_filename': 'js/benefitmy.js',
    }
}
