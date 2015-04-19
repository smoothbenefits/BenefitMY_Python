from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


def user_login(request, info_message=None):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the email and password provided by the user.
        # This information is obtained from the login form.
        userEmail = request.POST['email']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the email/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(email=userEmail, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(userEmail, password)

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
