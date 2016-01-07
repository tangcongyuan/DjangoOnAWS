from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def homepage(request):
	context = None
	return HttpResponse("Welcome to Eric's site!")