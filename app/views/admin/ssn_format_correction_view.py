import re

from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.person import Person


class SsnFormatCorrectionForAllView(APIView):

    def get(self, request, format=None):
        affected_person_ids = []
        all_persons = Person.objects.all()
        for person in all_persons:
            if (not person.is_ssn_format_valid()):
                # Resave it to ensure it goes through the model field 
                # normalization to correct the error
                person.save(update_fields=["ssn"])
                affected_person_ids.append(person.id)

        return Response(affected_person_ids)
