from rest_framework.response import Response

from django.http import Http404
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.core.mail import send_mail
from app.models.company import Company
from django.conf import settings

URL = settings.SITE_URL
SUBJECT = "Welcome to BenefitMy"
CONTENT = """

Hi %s,


We, BenefitMy LLC, are partnering with your employer, %s, to welcome you.  Your HR administrator has asked us to

     * Verify your employment eligibility in the US. so that you could start to work at the right time.  Please make sure you have all the necessary documents.
     * Collect the personal info in order to setup your health benefit.
     * Help you to enroll benefit plans for you and your family.

Here is your unique link to setup your account: %s.

If you have any questions, feel free to drop us an email.

Thanks,

BenefityMy

support@benefitmy.com
"""
FROM='Support@benefitmy.com'


def onboard_email(name, company_id, to, id):
    try:
        company = Company.objects.get(pk=company_id)
    except Company.DoesNotExist:
        raise Http404

    link = "%semployee/signup/%d" % (URL, id)

    c = CONTENT % (name, company.name, link)
    send_mail(SUBJECT, c, FROM, [to], fail_silently=False)


@api_view(['POST'])
def send_onboard_email(request):
    if request.method == 'POST':

        try:
            p = User.objects.get(email=request.DATA['email'])
        except User.DoesNotExist:
            raise Http404

        try:
            onboard_email(request.DATA['name'],
                          request.DATA['company_id'],
                          request.DATA['email'],
                          p.id)
            return Response(True)
        except StandardError:
            return Response(False)
