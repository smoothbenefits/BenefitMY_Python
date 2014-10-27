from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect


def index(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    # just go ahead and return the home html
    return render_to_response('dashboard.html', {}, context)
