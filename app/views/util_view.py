from rest_framework.response import Response

from django.http import Http404
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.core.mail import send_mail


@api_view(['POST'])
def send_onboard_email(request):
    if request.method == 'POST':

        SUBJECT = "s test"
        CONTENT = """
        Dear %s:
            Welcome. please click the link to login https://www.benefitmy.com/employee/signup/:%d
        """
        FROM='Support@benefitmy.com'


        def onboard_email(name, to, id):
            c = CONTENT % (name, id)
            send_mail(SUBJECT, c, FROM, [to], fail_silently=False)

        try:
            p = User.objects.get(email=request.DATA['email'])
        except User.DoesNotExist:
            raise Http404

        try:
            onboard_email(request.DATA['name'],
                          request.DATA['email'],
                          p.id)
            return Response("True")
        except StandardError:
            return Response("False")
