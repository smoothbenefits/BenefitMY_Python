from datetime import datetime
from StringIO import StringIO
from django.contrib.auth import get_user_model

from app.models.company_user import CompanyUser, USER_TYPE_ADMIN, USER_TYPE_BROKER
from app.models.company_features import CompanyFeatures

User = get_user_model()


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
