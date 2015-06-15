import httpagentparser
import json

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def index(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    agent = request.META['HTTP_USER_AGENT']
    parsed = httpagentparser.detect(agent)

    # For now, we only care about major version number
    version = int(parsed['browser']['version'].split('.')[0])
    browser = parsed['browser']['name']
    print browser
    print version

    if (IsSupported(browser, version)):
        # just go ahead and return the home html
        return render_to_response('home.html', {}, context)

    return render_to_response('warning.html', {}, context)

def IsSupported(browser, version):

	if (browser == 'Chrome' and version > 40):
		return True

	if (browser == 'Firefox' and version > 18):
		return True

	if (browser == 'Microsoft Internet Explorer' and version > 9):
		return True

	if (browser == 'Safari' and version > 4):
		return True

	return False