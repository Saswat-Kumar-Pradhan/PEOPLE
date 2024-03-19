from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def otp(request):
    return render(request, 'otp.html')

def signin(request):
    return render(request, 'signin.html')

def people(request):
    return render(request, 'people.html')

def peopleEdit(request):
    return render(request, 'peopleEdit.html')