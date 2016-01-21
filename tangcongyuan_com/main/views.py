# from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def homepage(request):
    context = None
    return render(request, 'main/index.html', context)


def more(request):
    context = {"string": "Here's more info about Eric!"}
    return render(request, 'main/more.html', context)


def google_web_master(request):
    return render(request, 'main/googlec41507c3bf67fa1c.html')


def bing_web_master(request):
    return render(request, 'main/BingSiteAuth.xml')
