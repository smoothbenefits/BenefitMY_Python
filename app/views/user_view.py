from rest_framework.views import APIView
from django.http import Http404
from django.shortcuts import render_to_response
from rest_framework.response import Response
from rest_framework import status

from app.models.company_user import CompanyUser
from app.models.company import Company
from app.models.user import User
from app.serializers.user_serializer import UserSerializer
from app.serializers.user_serializer import UserFamilySerializer
from app.serializers.person_serializer import PersonSerializer
from app.serializers.company_user_serializer import CompanyUserPostSerializer


class UserView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response({'user': serializer.data})


class UsersView(APIView):

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data})

    def post(self, request, format=None):
        if ("company" not in request.DATA or
            "company_user_type" not in request.DATA or
            "user" not in request.DATA or
            "first_name" not in request.DATA['user'] or
                "last_name" not in request.DATA['user']):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            c = Company.objects.get(pk=request.DATA['company'])
        except Company.DoesNotExist:
            raise Http404

        company_users = CompanyUser.objects.filter(
            company = request.DATA['company'])

        for c in company_users:
            if (c.company_user_type == request.DATA['company_user_type'] and
                    c.user.email == request.DATA['user']['email']):
                return Response(status=status.HTTP_409_CONFLICT)

        serializer = CompanyUserPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):

    def get(self, request, format=None):
        try:
            curUser = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            raise Http404
        company_users = CompanyUser.objects.filter(user=request.user.id)
        roles = []
        for q in company_users:
            if q.company_user_type not in roles:
                roles.append(q.company_user_type)

        serializer = UserSerializer(curUser)
        return Response({'user': serializer.data,
                         'roles': roles})


class UserFamilyView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserFamilySerializer(user)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        request.DATA['user'] = pk
        serializer = PersonSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView():
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
            profile_form = UserProfileForm(data=request.POST)

            # If the two forms are valid...
            if user_form.is_valid() and profile_form.is_valid():
                # Save the user's form data to the database.
                user = user_form.save()

                # Now we hash the password with the set_password method.
                # Once hashed, we can update the user object.
                user.set_password(user.password)
                user.save()

                # Now sort out the UserProfile instance.
                # Since we need to set the user attribute ourselves, we set commit=False.
                # This delays saving the model until we're ready to avoid integrity problems.
                profile = profile_form.save(commit=False)
                profile.user = user

                # Did the user provide a profile picture?
                # If so, we need to get it from the input form and put it in the UserProfile model.
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']

                # Now we save the UserProfile model instance.
                profile.save()

                # Update our variable to tell the template registration was successful.
                registered = True

            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
            else:
                print user_form.errors, profile_form.errors

        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()

        # Render the template depending on the context.
        return render_to_response('rango/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},context)

