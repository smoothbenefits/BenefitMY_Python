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


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x_qz2d46!0dmvk9(lb_c-z%r)&_jq8nl+-_fvsywp1+j+y5oj1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


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
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Smoothbenefits.urls'

WSGI_APPLICATION = 'Smoothbenefits.wsgi.application'


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

PIPELINE_COMPILERS = (
  'pipeline.compilers.coffee.CoffeeScriptCompiler',
  'pipeline.compilers.less.LessCompiler',
  'pipeline.compilers.sass.SASSCompiler',
)

PIPELINE_CSS_COMPRESSOR = ''
PIPELINE_JS_COMPRESSOR = ''


PIPELINE_CSS = {
    'home':{
        'source_filenames':(
            'stylesheets/front_end/users.css.scss',
            'stylesheets/shared/variables.css.scss',
            'stylesheets/shared/buttons.css.scss',
            'stylesheets/shared/components.css.scss',
            'stylesheets/shared/forms.css.scss',
            'stylesheets/shared/global.css.scss',
            'stylesheets/api.css.scss',
            'stylesheets/application.css.scss',
            'stylesheets/app.css',
            'stylesheets/bootstrap.css.scss',
            'stylesheets/framework_and_overrides.css.scss',
            'stylesheets/front_end.css.scss',
            'stylesheets/home.css',
            'stylesheets/layout.css',
            'stylesheets/pages.css',
            'stylesheets/users.css.scss',
        ),
        'output_filename': 'stylesheets/home.min.css',
    }
}
