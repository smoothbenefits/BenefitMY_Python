from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from app.service.data_modification_service import DataModificationService
from django.conf import settings


class UserDataChangeEmailView(APIView):
    def get(self, request, format=None):
        hours_back = request.GET.get('hoursback', 24)
        emails = request.GET.get('emails', None)
        if not emails:
            raise Http404
        target_emails = emails.split(',')
        mod_service = DataModificationService()
        mod_service.employee_modifications_notify_specific_target(hours_back*60, target_emails)
        return Response('OK')