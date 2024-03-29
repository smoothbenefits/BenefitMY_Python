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

# Environment Identification
IS_PRODUCTION_ENVIRONMENT = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x_qz2d46!0dmvk9(lb_c-z%r)&_jq8nl+-_fvsywp1+j+y5oj1'

# Hash key serving as the "secret word" to help hashing
HASH_KEY = '5e14ca8a-4a48-4cf7-aa3b-e207eb1a9adb'

# Default password for initial user account setup
DEFAULT_USER_PW = 'd4gf6u0hhfg48ds321cdsf'

# Global rekognition confidence threshold
GLOBAL_REKOGNITION_THRESHOLD = 60

# Whether debug logging should also output to console
LOG_TO_CONSOLE = False

# Allowed hosts names
ALLOWED_HOSTS = [ \
    'localhost', \
    '.benefitmy.com', \
    'benefitmy.com.', \
    '.workbenefitsme.com', \
    'workbenefitsme.com.', \
    '.workbenefits.me', \
    'workbenefits.me.', \
    '.heroku.com', \
    '.herokuapp.com' \
]

# Application definition
AUTH_USER_MODEL = 'app.AuthUser'

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
    'reversion',
    'django_cron',
    'cid',
)

# AWS settings
DEFAULT_AWS_REGION = 'us-west-2'

CID_GENERATE = True

PDFTK_BIN = './.apt/usr/bin/pdftk'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
    {
        'BACKEND': 'app.service.pdf_processing.pdf_tk_engine.PdftkEngine',
        'APP_DIRS': True,
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ENCRYPTED_FIELDS_KEYDIR = 'fieldkeys'


# Session expiration settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 8 * 60 * 60 #Set the expiry to 8 hrs for now.

# Email
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'frank.qiu@gmail.com'
EMAIL_HOST_PASSWORD = 'Shuibian2017'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SUPPORT_EMAIL_ADDRESS = 'support@workbenefits.me'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cid.middleware.CidMiddleware',
    'app.middlewares.hash_pk_validation_middleware.HashPkValidationMiddleware',
    'app.middlewares.logging_middleware.LoggingMiddleware',
    'app.middlewares.cors_middleware.CorsMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

CRON_CLASSES = [
    "app.scheduled_jobs.user_changes_notification.UserChangeNotifications",
    "app.scheduled_jobs.system_notifications.SystemNotifications",
    "app.scheduled_jobs.system_jobs.SystemJobs"
]

ROOT_URLCONF = 'Smoothbenefits.urls'

WSGI_APPLICATION = 'Smoothbenefits.wsgi.application'

# NOSE arguments for unit testing
NOSE_ARGS = ['--nocapture',
             '--nologcapture',]

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging settings
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
            'class': 'logentries.LogentriesHandler',
            'formatter': 'key-value-pair'
        },
        'console': {
            # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'level': 'DEBUG', # message level to be written to console
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
            'stylesheets/theapp.css',
        ),
        'output_filename': 'stylesheets/home.min.css',
    },
    'dashboard':{
        'source_filenames':(
            'stylesheets/theapp.css',
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
            'js/model_factories/benefitmyTimeTrackingModelFactories.js',
            'js/model_factories/benefitmyInsuranceCertificateModelFactories.js',
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
            'js/directives/BenefitGroupManager.js',
            'js/directives/CompanyServiceProviderManager.js',
            'js/directives/ConfirmUnsavedOnExit.js',
            'js/directives/ConfirmDialogOnClick.js',
            'js/directives/FamilyMemberManager.js',
            'js/directives/upload/UploadManager.js',
            'js/directives/upload/UploadAppFeatureManager.js',
            'js/directives/upload/UploadForUserManager.js',
            'js/directives/CustomDatePicker.js',
            'js/directives/PersonalInfoEditor.js',
            'js/directives/CompanyInfoEditor.js',
            'js/directives/benefit_election/CommuterElection.js',
            'js/directives/benefit_election/ExtraBenefitElection.js',
            'js/directives/SignaturePicker.js',
            'js/directives/DocumentUploadManager.js',
            'js/directives/EmployeeDocumentViewer.js',
            'js/directives/Edit1094c.js',
            'js/directives/GroupMemberLink.js',
            'js/directives/CompanyGroupSelection.js',
            'js/directives/CredentialUpdate.js',
            'js/directives/FileDownloadLink.js',
            'js/directives/hr/CompanyDepartmentManager.js',
            'js/directives/hr/CompanyJobManager.js',
            'js/directives/hr/CompanyDivisionManager.js',
            'js/directives/hr/TimeOffManager.js',
            'js/directives/hr/TimeOffRequestView.js',
            'js/directives/hr/CompanyTimeOffView.js',
            'js/directives/hr/TimesheetReportDownloadView.js',
            'js/directives/hr/EmployeesTimeOffInfo.js',
            'js/directives/hr/WorkTimesheetManager.js',
            'js/directives/DirectDepositManager.js',
            'js/directives/hr/WorkTimesheetWeekManager.js',
            'js/directives/hr/PhraseologyManager.js',
            'js/directives/hr/PhraseologyManager.js',
            'js/directives/hr/EmployeePhraseologyManager.js',
            'js/directives/hr/EmployeePhotoManager.js',
            'js/directives/BenefitSelectionViewer.js',
            'js/directives/contractor/ProjectManager.js',
            'js/directives/contractor/ProjectPayableManager.js',
            'js/directives/time_tracking/TimePunchCard.js',
            'js/directives/time_tracking/TimePunchCardAdmin.js',
            'js/directives/time_tracking/TimePunchCardWeeklyView.js',
            'js/directives/time_tracking/TimePunchCardAdminIndividual.js',
            'js/directives/time_tracking/EmployeesTimePunchCardSettingsList.js',
            'js/directives/OpenEnrollmentDefinition.js',
            'js/directives/payroll/AdvantagePayrollView.js',
            'js/directives/payroll/ConnectPayrollView.js',
            'js/directives/tax/StateTaxElectionView.js',
            'js/model_factories/benefitmyDomainModelFactories.js',
            'js/model_factories/benefitmyTimeTrackingModelFactories.js',
            'js/model_factories/benefitmyInsuranceCertificateModelFactories.js',
            'js/services/services.js',
            'js/pixel-admin.min.js',
            'js/jquery.scrollspy.js',
            'js/moment.min.js',
            'js/services/employeeBenefitElectionService.js',
            'js/services/EmployeePreDashboardValidationService.js',
            'js/services/BenefitElectionService.js',
            'js/services/CompanyService.js',
            'js/services/CompanyDepartmentService.js',
            'js/services/CompanyJobService.js',
            'js/services/CompanyDivisionService.js',
            'js/services/CompanyFeatureService.js',
            'js/services/CompanyEmployeeSummaryService.js',
            'js/services/CompanyServiceProviderService.js',
            'js/services/CompensationService.js',
            'js/services/DirectDepositService.js',
            'js/services/FsaService.js',
            'js/services/BasicLifeInsuranceService.js',
            'js/services/benefitDisplayService.js',
            'js/services/BrowserDetectionService.js',
            'js/services/documentTypeService.js',
            'js/services/PersonService.js',
            'js/services/UserService.js',
            'js/services/UploadService.js',
            'js/services/BenefitSummaryService.js',
            'js/services/CompanyBenefitAvailabilityService.js',
            'js/services/CompanyBenefitGroupService.js',
            'js/services/employeePayrollService.js',
            'js/services/tax/EmployeeTaxElectionService.js',
            'js/services/EmploymentProfileService.js',
            'js/services/EmployerEmployeeManagementService.js',
            'js/services/FeatureConfigurationService.js',
            'js/services/HealthBenefitsService.js',
            'js/services/StdService.js',
            'js/services/LtdService.js',
            'js/services/ApplicationFeatureService.js',
            'js/services/EmployeeProfileService.js',
            'js/services/LoggingService.js',
            'js/services/BrowserDetectionService.js',
            'js/services/SupplementalLifeInsuranceService.js',
            'js/services/SupplementalLifeInsuranceConditionService.js',
            'js/services/HraService.js',
            'js/services/HsaService.js',
            'js/services/CommuterService.js',
            'js/services/ExtraBenefitService.js',
            'js/services/DocumentService.js',
            'js/services/BenefitUpdateReasonService.js',
            'js/services/BenefitPolicyKeyService.js',
            'js/services/CompanyBenefitEnrollmentSummaryService.js',
            'js/services/BatchAccountCreationService.js',
            'js/services/BatchEmployeeOrganizationImportService.js',
            'js/services/Company1094CService.js',
            'js/services/Company1095CService.js',
            'js/services/Employee1095CService.js',
            'js/services/AgeRangeService.js',
            'js/services/EmployeeBenefitsAvailabilityService.js',
            'js/services/TemplateService.js',
            'js/services/SignatureService.js',
            'js/services/CommonUIWidgetService.js',
            'js/services/TimeOffService.js',
            'js/services/WorkTimesheetService.js',
            'js/services/UserOnboardingStepStateService.js',
            'js/services/UserCredentialService.js',
            'js/services/CompanyPersonnelsService.js',
            'js/services/UsStateService.js',
            'js/services/ContractorsService.js',
            'js/services/WorkersCompService.js',
            'js/services/ProjectService.js',
            'js/services/TimePunchCardService.js',
            'js/services/TimePunchCardSettingsService.js',
            'js/services/common/DateTimeService.js',
            'js/services/common/NumberService.js',
            'js/services/OpenEnrollmentDefinitionService.js',
            'js/services/IntegrationProviderService.js',
            'js/services/payroll_integration/AdvantagePayrollService.js',
            'js/services/payroll_integration/ConnectPayrollService.js'
            ),
        'output_filename': 'js/benefitmy.js',
    }
}
