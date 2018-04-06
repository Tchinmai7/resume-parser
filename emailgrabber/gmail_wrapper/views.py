# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import gmailfetch
# Create your views here.

def home(request):
	result={}
	result = gmailfetch.getMail()
	return HttpResponse(result)