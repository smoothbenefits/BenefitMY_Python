from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login

class AuthenticationResult(object):
    def __init__(self, logged_in, user, response):
        self.logged_in = logged_in
        self.user = user
        self.response = response


class AuthenticationService(object):

    def login(self, user_email, password, request):
        # Use Django's machinery to attempt to see if the email/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(email=user_email, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return AuthenticationResult(
                    True,
                    user,
                    HttpResponseRedirect('/dashboard/')
                )
            else:
                return AuthenticationResult(
                    False,
                    user,
                    HttpResponse("Your account is disabled.")
                )
        else:
            return AuthenticationResult(
                False,
                None,
                HttpResponseForbidden()
                )

