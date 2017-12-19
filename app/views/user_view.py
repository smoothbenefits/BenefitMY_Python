from rest_framework.views import APIView
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from rest_framework.authentication import BasicAuthentication

from django.db import transaction
from django.contrib.auth import get_user_model
from app.models.company_user import CompanyUser, USER_TYPE_ADMIN
from app.models.company import Company
from app.custom_authentication import AuthUserManager, AuthUser
from app.models.person import Person
from app.models.employee_profile import EmployeeProfile
from app.serializers.person_serializer import PersonSerializer, PersonSimpleSerializer
from app.serializers.user_serializer import UserSerializer
from app.serializers.employee_profile_serializer import EmployeeProfileSerializer
from app.serializers.company_user_serializer import CompanyRoleSerializer
from app.serializers.dtos.account_creation_data_serializer import AccountCreationDataSerializer
from app.views.util_view import onboard_email
from app.service.user_document_generator import UserDocumentGenerator
from django.conf import settings
from app.service.hash_key_service import HashKeyService
from app.service.account_creation_service import AccountCreationService
from app.service.authentication_service import AuthenticationService
from app.service.csrf_exempt_session_authentication import CsrfExemptSessionAuthentication
from app.service.application_feature_service import (
    ApplicationFeatureService,
    APP_FEATURE_PROJECTMANAGEMENT,
    APP_FEATURE_MOBILEPROJECTMANAGEMENT)
from app.service.project_service import ProjectService
from app.service.compensation_service import CompensationService
from app.view_models.person_info import PersonInfo

User = get_user_model()

def get_user_response_object(user, company_id=None):
    result = {}

    user_serializer = UserSerializer(user)
    result['user'] = user_serializer.data

    if company_id:
        company_user = CompanyUser.objects.get(user=user, company=company_id)
        company_role_serializer = CompanyRoleSerializer(company_user)
        result['company_role'] = company_role_serializer.data
    else:
        company_users = CompanyUser.objects.filter(user=user.id)
        roles = []
        for q in company_users:
            if q.company_user_type not in roles:
                comp_role = CompanyRoleSerializer(q)
                roles.append(comp_role.data)
        result['roles'] = roles

    persons = Person.objects.filter(user=user.id, relationship='self')
    if (len(persons) > 0):
        person_serializer = PersonSerializer(persons[0])
        result['person'] = person_serializer.data

        try:
            profile = EmployeeProfile.objects.get(person=persons[0].id)
            profile_serializer = EmployeeProfileSerializer(profile)
            result['profile'] = profile_serializer.data
        except EmployeeProfile.DoesNotExist:
            pass


    return result


class UserView(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response({'user': serializer.data})


class UsersView(APIView):

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data})

    @transaction.atomic
    def post(self, request, format=None):
        serializer = AccountCreationDataSerializer(data=request.DATA)
        if (not serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        account_info = serializer.object

        account_service = AccountCreationService()
        result = account_service.execute_creation(account_info)

        if (result.has_issue()):
            return Response(result.serialize_issues(), status=status.HTTP_400_BAD_REQUEST)

        # construct data back to consumer
        result_account_info = result.output_data
        user = User.objects.get(pk=result_account_info.user_id)
        response_data = get_user_response_object(user, result_account_info.company_id)

        return Response(response_data, status=status.HTTP_201_CREATED)


class CurrentUserView(APIView):

    def get(self, request, format=None):
        try:
            curUser = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            raise Http404

        result = get_user_response_object(curUser)

        return Response(result)


class UserCredentialView(APIView):

    '''
    This is the view to allow one user to change the password of another user.
    For now, password can be changed by the user him/herself or his/her admin.
    '''
    def put(self, request, format=None):

        target_user_id = request.DATA.get('target')

        initiator_user = AuthUser.objects.filter(email=request.user)
        initiator_user_id = initiator_user[0].id

        if self._is_valid_initiator(initiator_user_id, target_user_id):
            new_password = request.DATA.get('password')
            user = AuthUser.objects.get(pk=target_user_id)
            user.set_password(new_password)
            user.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=403)

    def _is_valid_initiator(self, initiator, target):

        if initiator == target:
            return True

        targetCompanyUsers = CompanyUser.objects.filter(user=target)
        initiatorCompanyUsers = CompanyUser.objects.filter(user=initiator)

        targetCompanies = []
        for companyUser in targetCompanyUsers:
            if companyUser.company not in targetCompanies:
                targetCompanies.append(companyUser.company.id)

        for companyUser in initiatorCompanyUsers:
            if companyUser.company.id in targetCompanies and companyUser.company_user_type == USER_TYPE_ADMIN:
                return True

        return False


class UserByCredentialView(APIView):
    hash_key_service = HashKeyService()

    '''
    This is the view class to provide the API endpoint for getting user information
    by providing the username and password of the user.
    Note: The information got from this end point is simplified.
    '''
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request, format=None):
        credential = request.DATA
        email = credential.get('email')
        password = credential.get('password')
        if not email or not password:
            return HttpResponse(status=401)
        auth_result = AuthenticationService().login(email, password, request)
        if auth_result.user:
            # Authentication successful.
            # Now get the user information
            result = self._get_user_data(auth_result.user)
            return Response(result)
        else:
            return HttpResponse(status=401)

    def _get_user_data(self, user):
        result = {}

        # User info
        user_info = {}

        ## Basic info
        user_info['user_id'] = user.id
        user_info['user_id_env_encode'] = self.hash_key_service.encode_key_with_environment(user.id)
        user_info['account_email'] = user.email

        ## Person and Compensation Info
        persons = Person.objects.filter(user=user.id, relationship='self')
        if (len(persons) > 0):
            person_model = persons[0]
            person_data = PersonInfo(person_model)
            user_info['first_name'] = person_data.first_name
            user_info['last_name'] = person_data.last_name

            compensation_info = CompensationService(person_model=person_model)
            hourly_rate = compensation_info.get_current_hourly_rate()
            if (hourly_rate):
                hourly_rate = round(hourly_rate, 2)
            user_info['hourly_rate'] = hourly_rate

        result['user_info'] = user_info

        # Company Info
        company_info = {}

        company_users = CompanyUser.objects.filter(user=user.id)
        company_id = None
        if (len(company_users) > 0):
            company_user = company_users[0]
            company_id = company_user.company_id
            company_info['company_id'] = company_id
            company_info['company_id_env_encode'] = self.hash_key_service.encode_key_with_environment(company_user.company_id)
            if (company_user.company):
                company_info['company_name'] = company_user.company.name

        result['company_info'] = company_info

        # Application Features
        application_features = None
        if (company_id):
            application_feature_service = ApplicationFeatureService()
            application_features = application_feature_service.get_complete_application_feature_status_by_company(company_id)
            result['app_features_info'] = application_features

        # Projects
        if (application_features
            and application_features[APP_FEATURE_PROJECTMANAGEMENT]):
            project_service = ProjectService()
            result['project_list'] = project_service.get_projects_by_company(company_id, active_only=True)

        return result
