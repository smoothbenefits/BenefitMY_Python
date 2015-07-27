from rest_framework.views import APIView
from django.http import Http404
from django.shortcuts import render_to_response
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from django.contrib.auth import get_user_model
from app.models.company_user import CompanyUser
from app.models.company import Company
from app.custom_authentication import AuthUserManager
from app.models.person import Person
from app.serializers.person_serializer import PersonSerializer, PersonSimpleSerializer
from app.serializers.user_serializer import UserSerializer
from app.serializers.employee_profile_serializer import EmployeeProfilePostSerializer
from app.serializers.company_user_serializer import CompanyRoleSerializer
from app.views.util_view import onboard_email
from app.service.user_document_generator import UserDocumentGenerator
from django.conf import settings
from app.service.hash_key_service import HashKeyService

User = get_user_model()

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
        if ("company" not in request.DATA or
            "company_user_type" not in request.DATA or
            "user" not in request.DATA or
            "first_name" not in request.DATA['user'] or
            "last_name" not in request.DATA['user']):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            c = Company.objects.get(pk=request.DATA['company'])
        except Company.DoesNotExist:
            raise Http404

        company_users = CompanyUser.objects.filter(
            company=request.DATA['company'])

        for c in company_users:
            if (c.company_user_type == request.DATA['company_user_type'] and
                    c.user.email == request.DATA['user']['email']):
                return Response(status=status.HTTP_409_CONFLICT)

        userManager = AuthUserManager()

        # Create the actual user data
        User.objects.create_user(request.DATA['user']['email'], settings.DEFAULT_USER_PW)
        if not userManager.user_exists(request.DATA['user']['email']):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = userManager.get_user(request.DATA['user']['email'])
        user.first_name = request.DATA['user']['first_name']
        user.last_name = request.DATA['user']['last_name']
        user.save()

        # Create the company_user data
        company_user = CompanyUser(company_id=request.DATA['company'],
                                   user=user,
                                   company_user_type=request.DATA['company_user_type'])

        if 'new_employee' in request.DATA:
            company_user.new_employee = request.DATA['new_employee']

        company_user.save()

        # Now create the person object
        person_data = {'first_name': request.DATA['user']['first_name'],
                       'last_name': request.DATA['user']['last_name'],
                       'user': user.id,
                       'relationship': 'self',
                       'person_type': 'primary_contact',
                       'company': request.DATA['company'],
                       'email':user.email}

        person_serializer = PersonSimpleSerializer(data=person_data)
        if person_serializer.is_valid():
            person_serializer.save()

        #Create the employee profile
        key_service = HashKeyService()
        profile_data = {
            'person': key_service.decode_key(person_serializer.data['id']),
            'company': request.DATA['company']
        }

        if 'annual_base_salary' in request.DATA and request.DATA['annual_base_salary'] > 0:
            profile_data['annual_base_salary'] = request.DATA['annual_base_salary']

        profile_serializer = EmployeeProfilePostSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()

        # Now check to see send email and create documents

        if company_user.company_user_type == 'employee':
            if 'send_email' in request.DATA and request.DATA['send_email']:
                # now try to create the onboard email for this user.
                try:
                    onboard_email("%s %s" % (user.first_name, user.last_name),
                                  request.DATA['company'],
                                  request.DATA['user']['email'],
                                  user.id
                                  )
                except StandardError:
                    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

            if ('create_docs' in request.DATA and
                'fields' in request.DATA and
                request.DATA['create_docs']):
                #Let's create the documents for this new user
                try:
                    doc_gen = UserDocumentGenerator(company_user.company, user)
                    doc_gen.generate_all_document(request.DATA['fields'])
                except Exception as e:
                    print "Exception happend on User Document Generation! Exception is {}".format(e)

        #construct data back to consumer
        user_serializer = UserSerializer(user)
        company_role_serializer = CompanyRoleSerializer(company_user)
        response_data = {
            'user': user_serializer.data,
            'company_role': company_role_serializer.data,
            'person': person_serializer.data,
            'profile': profile_serializer.data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class CurrentUserView(APIView):

    def get(self, request, format=None):
        try:
            curUser = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            raise Http404

        result = {}

        serializer = UserSerializer(curUser)
        result['user'] = serializer.data

        company_users = CompanyUser.objects.filter(user=request.user.id)
        roles = []
        for q in company_users:
            if q.company_user_type not in roles:
                comp_role = CompanyRoleSerializer(q)
                roles.append(comp_role.data)
        result['roles'] = roles

        # Get Person Data
        persons = Person.objects.filter(user=request.user.id, relationship='self')
        if (len(persons) > 0):
            personSerializer = PersonSerializer(persons[0])
            result['person'] = personSerializer.data

        return Response(result)
