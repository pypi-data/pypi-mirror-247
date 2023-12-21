from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from stela_control.forms import RegistrationForm, UserLoginForm
# Create your views here.
def login(request):
    form=UserLoginForm()
    context = {
       'form': form
    }
    return render(request, 'home/auth/login/index.html', context)

def account_register(request):
    form=RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'home/auth/registration/index.html', context)

def logout(request):
    logout(request)
    return redirect('/auth/login/')