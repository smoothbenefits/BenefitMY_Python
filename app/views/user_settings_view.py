from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from rest_framework.response import Response


class SettingView(APIView):
    def post(self, request, format=None):
        username = request.DATA['username']
        current_password = request.DATA['current_password']
        new_password = request.DATA['new_password']
        confirm_new_password = request.DATA['confirm_new_password']
        if new_password != confirm_new_password:
            return Response({'error':'The new password and confirm do not match'}, status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=username, password=current_password)
        if user and user.is_active:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return Response({'success':'updated'}, status.HTTP_200_OK)
        else:
            return Response({'error':'The user do not authenticate'}, status.HTTP_401_UNAUTHORIZED)

    def get(self, request, format=None):
        return Response({'success':'setting active'}, status.HTTP_200_OK)
