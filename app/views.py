from django.shortcuts import render, redirect
from .forms import RegistrationForm, ProfileForm
from django.http import HttpResponseServerError
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from datetime import datetime
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
                sub = 'User Verification'
                msg = f'''
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    color: #333;
                                    line-height: 1.6;
                                    padding: 20px;
                                }}
                                .container {{
                                    max-width: 600px;
                                    margin: auto;
                                    padding: 20px;
                                    background-color: #f9f9f9;
                                    border-radius: 10px;
                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                }}
                                .header {{
                                    text-align: center;
                                    margin-bottom: 20px;
                                }}
                                .header h1{{
                                    font-size: 40px;
                                    font-weight: bolder;
                                }}
                                .otp {{
                                    font-size: 24px;
                                    font-weight: bold;
                                    color: #007bff;
                                    text-align: center;
                                }}
                                .button {{
                                    display: inline-block;
                                    margin-top: 20px;
                                    padding: 10px 20px;
                                    background-color: #007bff;
                                    color: white;
                                    text-decoration: none;
                                    border-radius: 5px;
                                }}
                                .footer {{
                                    margin-top: 30px;
                                    text-align: center;
                                    color: #666;
                                    font-size: 12px;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <div class="header">
                                    <h1>PEOPLE</h1>
                                    <p>Secure your account with this one-time password (OTP).</p>
                                </div>
                                <p>Hello,</p>
                                <p>Thank you for joining us! To complete your registration and secure your account, please use the following OTP:</p>
                                <p class="otp">{otp}</p>
                                <p>Enter this code on the verification page to confirm your identity.</p>
                                <center><a href="https://www.yourwebsite.com/verify" class="button">Verify Now</a></center>
                                <div class="footer">
                                    <p>If you did not request this verification, please ignore this email.</p>
                                    <p>&copy; 2024 . PEOPLE . All rights reserved.</p>
                                </div>
                            </div>
                        </body>
                        </html>
                        '''

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
        user_entered_otp = request.POST.get('otp')
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
        try:
            profile = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            profile = None
        if profile and profile.password == password:
            request.session['profile_id'] = profile.id
            return redirect('peopleEdit')  # Redirect to dashboard after successful login
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'signin.html')

def people(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if profile.dob:
        dob_year = profile.dob.year
        current_year = datetime.now().year
        age = current_year - dob_year
        if (datetime.now().month, datetime.now().day) < (profile.dob.month, profile.dob.day):
            age -= 1
    else:
        age = None
    return render(request, 'people.html', {'profile': profile, 'age': age, 'first_name': profile.name.split()[0]})

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
        if form.is_valid():
            print(form.cleaned_data.get('portfolio_availability'))
            form.save()
            messages.success(request, 'Details Saved Successfully.')
            return redirect('people',profile_id)
        else:
            print(form.errors)
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'peopleEdit.html', {'profile': profile})

def logout(request):
    del request.session['profile_id']
    return redirect('index')