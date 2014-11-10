from rest_framework.response import Response

from django.http import Http404
from rest_framework.decorators import api_view
from app.models.person import Person
from app.util.email import onboard_email


@api_view(['POST'])
def send_onboard_email(request):
    if request.method == 'POST':
        try:
            p = Person.objects.get(email=request.DATA['email'])
        except Person.DoesNotExist:
            raise Http404

        try:
            onboard_email(request.DATA['name'],
                          request.DATA['to'],
                          p.id)
            return Response("email send")
        except StandardError:
            return Response("email failed")
