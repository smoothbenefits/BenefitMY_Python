from rest_framework.views import APIView
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from rest_framework.authentication import BasicAuthentication

from django.db import transaction
from django.contrib.auth import get_user_model
from app.models.company_user import CompanyUser
from app.models.company import Company
from app.custom_authentication import AuthUserManager
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
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
        result['user_id'] = user.id
        result['user_id_env_encode'] = self.hash_key_service.encode_key_with_environment(user.id)
        result['account_email'] = user.email

        # Company Info
        company_users = CompanyUser.objects.filter(user=user.id)
        if (len(company_users) > 0):
            result['company_id'] = company_users[0].company_id
            result['company_id_env_encode'] = self.hash_key_service.encode_key_with_environment(company_users[0].company_id)

        # Person and Compensation Info
        persons = Person.objects.filter(user=user.id, relationship='self')
        if (len(persons) > 0):
            person_data = PersonInfo(persons[0])
            result['first_name'] = person_data.first_name
            result['last_name'] = person_data.last_name
            result['hourly_rate'] = person_data.get_current_hourly_rate()

        return result
