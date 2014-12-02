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
from app.serializers.user_serializer import UserSerializer
from app.serializers.user_serializer import UserFamilySerializer
from app.serializers.person_serializer import PersonFullPostSerializer
from app.views.util_view import onboard_email


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

        create_user(request.DATA['user']['email'], '123456')
        if not user_exists(request.DATA['user']['email']):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = get_user(request.DATA['user']['email'])
        user.first_name = request.DATA['user']['first_name']
        user.last_name = request.DATA['user']['last_name']
        user.save()

        company_user = CompanyUser(company_id=request.DATA['company'],
                                   user=user,
                                   company_user_type=request.DATA['company_user_type'])
        company_user.save()

        serializer = UserSerializer(user)
        try:
            onboard_email("%s %s" % (user.first_name, user.last_name),
                          request.DATA['company'],
                          request.DATA['user']['email'],
                          user.id
                          )
        except StandardError:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

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
                roles.append(q.company_user_type)

        serializer = UserSerializer(curUser)
        return Response({'user': serializer.data,
                         'roles': roles})


class UserFamilyView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserFamilySerializer(user)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        request.DATA['user'] = pk
        serializer = PersonFullPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
