from contextlib import redirect_stdout
from django.shortcuts import render,redirect
from .forms import ContactForm
from .forms import RegistrationForm
from .models import Programs, Leadership
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber
def home(request):
    return render(request, 'home.html', {'active_page': 'home'})

def about_us(request):
    leadership = Leadership.objects.all()
    return render(request, 'aboutus.html', {'active_page': 'about', 'leadership':leadership})

@login_required
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            if request.user.is_authenticated:
                contact_message.user = request.user
            contact_message.save()

            # Send email to special users
            subject = f"New Contact Form Submission:"
            message = f"Name: {contact_message.name}\nEmail: {contact_message.email}\nMessage: {contact_message.message}"
            print(message)
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = ['tatvajoshi0@gmail.com']  # Add email addresses of special users
            send_mail("A New Inquiry", message, from_email, recipient_list)
            messages.success(request, 'Your message has been sent successfully!')
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

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if email is already subscribed
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.info(request, 'You are already subscribed to the newsletter.')
            else:
                subscriber = form.save()
                # Send a confirmation email
                send_mail(
                    'Newsletter Subscription Confirmation',
                    'Thank you for subscribing to our newsletter!',
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                    fail_silently=False,
                )
                messages.success(request, 'Subscribed successfully! A confirmation email has been sent to you.')
            return redirect('home')  # Redirect to a page or the same page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NewsletterSignupForm()

    return render(request, 'home.html', {'form': form})