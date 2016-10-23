from django.template import RequestContext
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from app.service.authentication_service import AuthenticationService


def user_login(request, info_message=None):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the email and password provided by the user.
        # This information is obtained from the login form.
        userEmail = request.POST['email'].lower()
        password = request.POST['password']

        auth_result = AuthenticationService().login(userEmail, password, request)

        if auth_result.user:
            return auth_result.response
        else:
            external_message = "The combination of your email and password is not correct"
            return render_to_response('login.html', {'message':external_message}, context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        infoMessage = ""
        if (info_message) :
            infoMessage = urlsafe_base64_decode(info_message)
        return render_to_response('login.html', {'message':'', 'info_message':infoMessage}, context)

@require_http_methods(['DELETE'])
@csrf_exempt
def user_logout(request):
    logout(request)
    return HttpResponse("done")
