import random
import string

from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password


class PasswordGeneratorView(APIView):

    def get(self, request, num_passwords, format=None):
        result = {}
        for i in range(0, int(num_passwords)):
            new_pw = self.__random_string(8)
            salt = self.__random_string(5)
            new_pw_hash = make_password(password=new_pw, salt=salt)
            result[new_pw] = new_pw_hash

        return Response(result)

    def __random_string(self, length):
        return ''.join(random.choice(string.lowercase + string.digits) for i in range(length))
