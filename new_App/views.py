from contextlib import redirect_stdout
from django.shortcuts import render,redirect
from .forms import ContactForm
from .forms import RegistrationForm
from .models import Programs, Leadership


def home(request):
    return render(request, 'home.html', {'active_page': 'home'})

def about_us(request):
    leadership = Leadership.objects.all()
    return render(request, 'aboutus.html', {'active_page': 'about', 'leadership':leadership})

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()
    
    return render(request, 'contactus.html', {'form': form, 'active_page': 'contact'})

def contact_success(request):
    return render(request, 'contact_success.html')
    

def programs(request):
    programs = Programs.objects.all()
    return render(request, 'programs.html', {'active_page': 'programs', 'programs':programs})

def get_involved(request):
    return render(request, 'getinvolved.html', {'active_page': 'getinvolved'})

def events(request):
    return render(request, 'events.html', {'active_page': 'events'})

def login_view(request):
    return render(request, 'login.html', {'active_page': 'login'})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form, 'active_page': 'register'})

def resources_view(request):
    return render(request, 'resources.html', {'active_page': 'resources'})