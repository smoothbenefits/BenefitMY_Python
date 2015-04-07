from rest_framework.views import APIView
from django.http import Http404
from django.shortcuts import render_to_response
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from emailusernames.utils import (
    create_user,
    get_user,
    user_exists)
from app.models.company_user import CompanyUser
from app.models.company import Company
from app.models.user import User
from app.models.person import Person
from app.serializers.user_serializer import UserSerializer
from app.serializers.user_serializer import UserFamilySerializer
from app.serializers.person_serializer import PersonFullPostSerializer
from app.serializers.company_user_serializer import CompanyRoleSerializer
from app.views.util_view import onboard_email
from app.service.user_document_generator import UserDocumentGenerator
from django.conf import settings


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

        create_user(request.DATA['user']['email'], settings.DEFAULT_USER_PW)
        if not user_exists(request.DATA['user']['email']):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = get_user(request.DATA['user']['email'])
        user.first_name = request.DATA['user']['first_name']
        user.last_name = request.DATA['user']['last_name']
        user.save()

        company_user = CompanyUser(company_id=request.DATA['company'],
                                   user=user,
                                   company_user_type=request.DATA['company_user_type'])

        if 'new_employee' in request.DATA:
            company_user.new_employee = request.DATA['new_employee']

        company_user.save()

        serializer = UserSerializer(user)

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

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CurrentUserView(APIView):

    def get(self, request, format=None):
        try:
            curUser = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            raise Http404
        company_users = CompanyUser.objects.filter(user=request.user.id)
        roles = []
        for q in company_users:
            if q.company_user_type not in roles:
                comp_role = CompanyRoleSerializer(q)
                roles.append(comp_role.data)

        serializer = UserSerializer(curUser)
        return Response({'user': serializer.data,
                         'roles': roles})


class UserFamilyView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_person_by_user(self, user, relation_to_user):
        try:
            person_set=Person.objects.filter(user=user, relationship=relation_to_user)
            if person_set:
                return person_set[0]
            else:
                return None
        except Person.DoesNotExist:
            return None


    def get(self, request, pk, format=None):
        print request.user
        print pk
        user = self.get_object(pk)
        serializer = UserFamilySerializer(user)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        user = self.get_object(pk)
        request.DATA['user'] = pk
        relationship = request.DATA['relationship']
        if relationship != 'dependent':
            person = self.get_person_by_user(user, relationship)
            if person:
                serializer = PersonFullPostSerializer(person, data=request.DATA)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = PersonFullPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
