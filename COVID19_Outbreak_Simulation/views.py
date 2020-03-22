from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import main


# Create your views here.


def index(request):
    # later it will be a request to database.
    context = {}
    return render(request, 'main_page/index.html', context)

global value

def calculate(request):
    global value
    get = request.GET.get('user_input')

    value = main.connect(get)
    return JsonResponse({'value': value})

