from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm  


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect("home:home_page")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/sign_up.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user = authenticate(username=user.username, password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                messages.success(request, "Signin successful!")
                return redirect("home:home_page")
            else:
                messages.error(request, "Worng username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/sign_in.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home:home_page")
