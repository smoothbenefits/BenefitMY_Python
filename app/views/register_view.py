from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from app.forms import UserForm
from emailusernames.utils import create_user, get_user, user_exists
from app.models.user import User


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid():
            create_user(request.POST['email'], request.POST['password'])

            registered = True
            # Update our variable to tell the template registration was successful.
            return redirect('/login')
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response('register.html',{'user_form': user_form, 'registered': registered},context)


def register_employee(request, user_id):
    context = RequestContext(request)
    registered = False
    user_email = ""
    error_message = ""

    try:
        employee_user = User.objects.get(pk=user_id)
        user_email = employee_user.email
    except User.DoesNotExist:
            error_message = "We cannot find the user based on the URL. Please contact your HR."

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        confirm_password = request.POST['confirm_password']
        user_password = request.POST['password']
        if not user_form.is_valid():
            error_message = "The Email and Password you have entered is invalid. Please try again."

        if user_password != confirm_password:
            error_message = "The passwords you have entered do not match. Please try again."

        if error_message:
            return render_to_response('register.html',{'user_form': user_form, 'registered': registered, 'user_email':user_email, 'errorMessage':error_message},context)
        else:
            employee_user.email = request.POST['email']
            employee_user.set_password(user_password)
            employee_user.save()
            return redirect('/login')
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response('register.html',{'user_form': user_form, 'registered': registered, 'user_email':user_email, 'errorMessage':error_message},context)
