from django.utils import timezone
from django.shortcuts import render,redirect
from .forms import ContactForm
from .forms import RegistrationForm, EventForm
from .models import Programs, Leadership, Event
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

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
            username = form.cleaned_data['username']
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form, 'active_page': 'register', 'username':username})

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

import stripe
@login_required(login_url='login')
def product_page(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	if request.method == 'POST':
		checkout_session = stripe.checkout.Session.create(
			payment_method_types = ['card'],
			line_items = [
				{
					'price': settings.PRODUCT_PRICE,
					'quantity': 1,
				},
			],
			mode = 'payment',
			customer_creation = 'always',
			success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
			cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
		)
		return redirect(checkout_session.url, code=303)
	return render(request, 'product_page.html')

from .models import UserPayment
## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    # Create a new UserPayment record
    user_payment = UserPayment.objects.create(
        app_user=request.user,
        stripe_charge_id=checkout_session_id,
        amount=session.amount_total / 100,  # Convert from cents to dollars
        currency=session.currency,
        success=True
    )
    return render(request, 'payment_successful.html', {'customer': customer})


def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	return render(request, 'payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        # Mark the payment as successful in the database
        try:
            user_payment = UserPayment.objects.get(stripe_charge_id=session_id)
            user_payment.success = True
            user_payment.save()
        except UserPayment.DoesNotExist:
            pass
    return HttpResponse(status=200)


def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events_page')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

def events_page(request):
    upcoming_events = Event.objects.filter(event_date__gte=timezone.now()).order_by('event_date')
    events = Event.objects.all()
    past_events = Event.objects.filter(event_date__lt=timezone.now()).order_by('-event_date')
    return render(request, 'events_page.html', {'upcoming_events': upcoming_events, 'past_events': past_events})