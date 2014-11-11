from django.core.mail import send_mail

SUBJECT="s test"
CONTENT="""
Dear %s:
    Welcome. please click the link to login https://xxxxxx.com/:%d
"""
FROM='xxx@gmail.com'


def onboard_email(name, to, id):
    c = CONTENT % (name, id)
    send_mail(SUBJECT, c, FROM, [to], fail_silently=False)
