from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login


# Create your views here.


def index(request):
    # later it will be a request to database.
    context = {}
    return render(request, 'main_page/index.html', context)