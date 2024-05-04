from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin, login_url='login')  # Specify the login URL
def profile(request):
    return render(request, 'Dashboard.html')

def is_user(user):
    return user.is_authenticated and not user.is_staff

@user_passes_test(is_user, login_url='login')  # Specify the login URL
def user_page(request):
    return render(request, 'display_questions.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')  
        email = request.POST.get('email') 
        password = request.POST.get('pass') 
        
        new_user = User.objects.create_user(fname, email, password)
        new_user.first_name = fname
        
        new_user.save()
        return redirect('login')

    return render(request, 'register.html')

def coustomlogin(request):
    if request.method == 'POST':
        name = request.POST.get('fname')
        password = request.POST.get('pass')

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect(request.GET.get('next', 'profile'))
            else:
                return redirect('next_random_question')
        else:
            return HttpResponse('Error, user does not exist')

    return render(request, 'login.html')
