# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, re
from django.views import View
from django.shortcuts import render_to_response
from django.http import HttpResponse


# Create your views here.

def StagerView(request):
    hostname = request.META['HTTP_HOST']
    response = render_to_response('template.py', context={'hostname' : hostname})
    response['Content-Disposition'] = 'attatchment; filename=stager.py'
    return response

def LatestView(request):
    path = os.getcwd() + "/agent/dist/"
    whls = os.listdir(path)
    p = re.compile("C2F_Agent-(\d.\d.\d)")

    versions = map(lambda x: "".join(p.match(x).group(1).split(".")), whls)
    latest = max(versions)
    whl = "Agent-%s-py2-none-any.whl" % ".".join(list(latest))

    with open(path + whl, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/binary")
        response['Content-Disposition'] = 'inline; filename=' + whl
        return response

