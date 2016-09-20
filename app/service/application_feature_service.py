from datetime import datetime
from StringIO import StringIO
from django.contrib.auth import get_user_model

from app.models.company_user import CompanyUser, USER_TYPE_ADMIN, USER_TYPE_BROKER
from app.models.company_features import CompanyFeatures

User = get_user_model()

# List of features
APP_FEATURE_FSA = 'FSA'
APP_FEATURE_DD = 'DD'
APP_FEATURE_MEDICALBENEFIT = 'MedicalBenefit'
APP_FEATURE_DENTALBENEFIT = 'DentalBenefit'
APP_FEATURE_VISIONBENEFIT = 'VisionBenefit'
APP_FEATURE_I9 = 'I9'
APP_FEATURE_MANAGER = 'Manager'
APP_FEATURE_DEPOSIT = 'Deposit'
APP_FEATURE_BASICLIFE = 'BasicLife'
APP_FEATURE_OPTIONALLIFE = 'OptionalLife'
APP_FEATURE_STD = 'STD'
APP_FEATURE_LTD = 'LTD'
APP_FEATURE_HRA = 'HRA'
APP_FEATURE_W4 = 'W4'
APP_FEATURE_ADAD = 'ADAD'
APP_FEATURE_BENEFITSFORFULLTIMEONLY = 'BenefitsForFullTimeOnly'
APP_FEATURE_COMMUTER = 'Commuter'
APP_FEATURE_EXTRABENEFIT = 'ExtraBenefit'
APP_FEATURE_TIMEOFF = 'Timeoff'
APP_FEATURE_WORKTIMESHEET = 'WorkTimeSheet'
APP_FEATURE_WORKTIMESHEETNOTIFICATION = 'WorkTimeSheetNotification'
APP_FEATURE_RANGEDTIMECARD = 'RangedTimeCard'
APP_FEATURE_PROJECTMANAGEMENT = 'ProjectManagement'
APP_FEATURE_MOBILEPROJECTMANAGEMENT = 'MobileProjectManagement'
APP_FEATURE_SHOWDISABLEDFEATURESFOREMPLOYER = 'ShowDisabledFeaturesForEmployer'

# Feature categorization by expected default behavior
APP_FEATURES_DEFAULT_ENABLED = [
    APP_FEATURE_WORKTIMESHEET,
    APP_FEATURE_MOBILEPROJECTMANAGEMENT,
    APP_FEATURE_FSA,
    APP_FEATURE_DD,
    APP_FEATURE_MEDICALBENEFIT,
    APP_FEATURE_DENTALBENEFIT,
    APP_FEATURE_VISIONBENEFIT,
    APP_FEATURE_I9,
    APP_FEATURE_MANAGER,
    APP_FEATURE_DEPOSIT,
    APP_FEATURE_BASICLIFE,
    APP_FEATURE_OPTIONALLIFE,
    APP_FEATURE_STD,
    APP_FEATURE_LTD,
    APP_FEATURE_HRA,
    APP_FEATURE_W4,
    APP_FEATURE_ADAD,
    APP_FEATURE_COMMUTER,
    APP_FEATURE_EXTRABENEFIT,
    APP_FEATURE_TIMEOFF,
    APP_FEATURE_SHOWDISABLEDFEATURESFOREMPLOYER
]

APP_FEATURES_DEFAULT_DISABLED = [
    APP_FEATURE_BENEFITSFORFULLTIMEONLY,
    APP_FEATURE_WORKTIMESHEETNOTIFICATION,
    APP_FEATURE_RANGEDTIMECARD,
    APP_FEATURE_PROJECTMANAGEMENT
]


class ApplicationFeatureService(object):

    def get_company_list_with_feature_disabled(self, feature_name):
        return self._get_company_list_with_feature_status(feature_name, False)

    def get_company_list_with_feature_enabled(self, feature_name):
        return self._get_company_list_with_feature_status(feature_name, True)

    def _get_company_list_with_feature_status(self, feature_name, feature_status):
        company_list = []

        company_features = self._get_company_features_by_feature_name(feature_name)
        company_features = company_features.filter(feature_status=feature_status)

        for company_feature in company_features:
            company_list.append(company_feature.company.id)

        return company_list

    def _get_company_features_by_feature_name(self, feature_name):
        return CompanyFeatures.objects.filter(company_feature__feature__iexact=feature_name.lower())

    def get_complete_application_feature_status_by_company(self, company_id):
        result = {}

        # Setup baseline
        for feature in APP_FEATURES_DEFAULT_ENABLED:
            result[feature] = True

        for feature in APP_FEATURES_DEFAULT_DISABLED:
            result[feature] = False

        company_features = CompanyFeatures.objects.filter(company=company_id)
        for company_feature in company_features:
            result[company_feature.company_feature.feature] = company_feature.feature_status

        return result
