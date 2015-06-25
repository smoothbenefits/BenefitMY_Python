from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from app.service.browser_detection_service import IsBrowserSupported

def index(request):

    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    agent = request.META['HTTP_USER_AGENT']
    if not IsBrowserSupported(agent):
        return render_to_response('warning.html', {}, context)

    if not request.user.is_authenticated():
        return redirect('/login/')

    # just go ahead and return the home html
    return render_to_response('dashboard.html', {}, context)
