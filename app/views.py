from django.shortcuts import render, redirect
from .forms import RegistrationForm, ProfileForm
from django.http import HttpResponseServerError
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from .models import *
import traceback
import random

# Create your views here.

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        try:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                # Generate OTP
                otp = random.randint(100000, 999999)

                # Prepare email subject and message
                sub = 'Blog Post User Verification'
                msg = f'<p>Your OTP: <b>{otp}</b></p>'
                from_email = 'saswatkumar059@gmail.com'
                
                # Send email
                send_mail(sub, msg, from_email, [form.cleaned_data.get('email')], html_message=msg)

                # Store form data and OTP in session
                request.session['signup_form_data'] = form.cleaned_data
                request.session['otp'] = otp

                return redirect('otp')
        except Exception as e:
            traceback.print_exc()
            return HttpResponseServerError("An unexpected error occurred. Please try again later.")
    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {'form': form})

def otp(request):
    form_data = request.session.get('signup_form_data')
    otp = request.session.get('otp')

    if not form_data or not otp:
        return redirect('signup')

    if request.method == 'POST':
        user_entered_otp = request.POST.get('otp')  # Assuming OTP is submitted via a form field named 'otp'
        if user_entered_otp == str(otp):
            try:
                profile = Profile.objects.create(
                    name=form_data.get('name'),
                    email=form_data.get('email'),
                    password=form_data.get('password'),
                )
                del request.session['signup_form_data']
                del request.session['otp']

                return redirect('index')
            except Exception as e:
                traceback.print_exc()
                return HttpResponseServerError("An unexpected error occurred while saving data.")

    return render(request, 'otp.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("hello")
        try:
            profile = Profile.objects.get(email=email)
            print("hello2")
        except Profile.DoesNotExist:
            profile = None
        if profile and profile.password == password:
            request.session['profile_id'] = profile.id
            return redirect('peopleEdit')  # Redirect to dashboard after successful login
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'signin.html')

def people(request):
    return render(request, 'people.html')

def peopleEdit(request):
    if 'profile_id' not in request.session:
        return redirect('signin')
    try:
        profile_id = request.session['profile_id']
        profile = Profile.objects.get(id=profile_id)
    except (KeyError, Profile.DoesNotExist):
        return redirect('signin')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        print("out")
        if form.is_valid():
            print("in")
            form.save()
            messages.success(request, 'Details Saved Successfully.')
            return redirect('people')
        else:
            print(form.errors)
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'peopleEdit.html', {'profile': profile})

def logout(request):
    del request.session['profile_id']
    return redirect('index')