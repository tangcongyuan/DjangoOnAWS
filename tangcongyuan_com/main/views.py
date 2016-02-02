# from django.http import HttpResponse, JsonResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError


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

def contact_me(request):
    name = request.POST.get('name', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')
    if name and message and from_email:
        try:
            send_mail("Message from: " + name, message, from_email, ['erictang@tangcongyuan.com'])
            send_mail("Confirmation email sent", "Hello "+name+",\nYour email has been recieved by me. I'll get back to you asap. Thanks!\nEric (Congyuan) Tang", "erictang@tangcongyuan.com", [from_email])
        except BadHeaderError:
            return JsonResponse({'message': 'Invalid header found.'})
        return JsonResponse({'message': 'Message successfully sent.'})
    return JsonResponse({'message': 'Something terrible happend!'})
