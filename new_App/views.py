from django.utils import timezone
from django.shortcuts import render,redirect
from .forms import ContactForm
from .forms import RegistrationForm, EventForm
from .models import Programs, Leadership, Event, WebData
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Home View
def home(request):
    return render(request, 'home.html', {'active_page': 'home'})

# About Us View
def about_us(request):
    leadership = Leadership.objects.all()
    visiondata=WebData.objects.get(title = 'vision')
    missiondata=WebData.objects.get(title = 'mission')
    aboutdata = WebData.objects.get(title='about_text')
    aboutheader = WebData.objects.get(title = 'header')
    ss = WebData.objects.get(title = 'successstory')
    cs = WebData.objects.get(title = 'casestudy')
    sc = WebData.objects.get(title = 'satisfied_clients')
    context = {
        'leadership': leadership,
        'vision': visiondata,
        'mission':missiondata,
        'about':aboutdata,
        'header':aboutheader,
        'active_page': 'about',
        'ss1':ss,
        'cs1':cs,
        'sc1':sc
    }
    return render(request, 'aboutus.html', context)

# Contact Us View
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
    
# Programs View
def programs(request):
    programs = Programs.objects.all()
    return render(request, 'programs.html', {'active_page': 'programs', 'programs':programs})

# Get Involved View
# def get_involved(request):
#     benefit_data = WebData.objects.filter(page_name = 'GetInvolved')
#     impact_data = WebData.objects.filter(page_name = 'GetInvolved_Impact')
#     context = {
#         'benefit_data':benefit_data,
#         'impact_data':impact_data,
#         'active_page': 'getinvolved'
#     }
#     return render(request, 'getinvolved.html', context)

def events(request):
    upcoming_events = Event.objects.filter(event_date__gte=timezone.now()).order_by('event_date')
    past_events = Event.objects.filter(event_date__lt=timezone.now()).order_by('-event_date')

    # Pagination for upcoming events
    paginator_upcoming = Paginator(upcoming_events, 5)  # Show 5 events per page
    page = request.GET.get('page_upcoming')
    try:
        upcoming_events = paginator_upcoming.page(page)
    except PageNotAnInteger:
        upcoming_events = paginator_upcoming.page(1)
    except EmptyPage:
        upcoming_events = paginator_upcoming.page(paginator_upcoming.num_pages)

    # Pagination for past events
    paginator_past = Paginator(past_events, 5)  # Show 5 events per page
    page = request.GET.get('page_past')
    try:
        past_events = paginator_past.page(page)
    except PageNotAnInteger:
        past_events = paginator_past.page(1)
    except EmptyPage:
        past_events = paginator_past.page(paginator_past.num_pages)

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'active_page':'events'
    }

    return render(request, 'events.html', context)

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
# @login_required(login_url='/accounts/login/')
def getinvolved_page(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    benefit_data = WebData.objects.filter(page_name = 'GetInvolved')
    impact_data = WebData.objects.filter(page_name = 'GetInvolved_Impact')
    context = {
        'benefit_data':benefit_data,
        'impact_data':impact_data,
        'active_page': 'getinvolved'
    }
    if request.method == 'POST':
        donation_amount = int(request.POST.get('donation_amount')) * 100
        donation_type = request.POST.get('donation_type')
        email = request.POST.get('email')
        if donation_type == 'recurring':
            # Create a Stripe customer
            customer = stripe.Customer.create(email=email)
            # Create a Stripe product if not already created
            product = stripe.Product.create(name='Recurring Donation')
            
            # Create a Stripe price object for the recurring payment
            price = stripe.Price.create(
                unit_amount=donation_amount,
                currency="cad",
                recurring={"interval": "month"},
                product=product.id,
            )
            
            # Create a Stripe checkout session for the subscription
            checkout_session = stripe.checkout.Session.create(
                customer=customer.id,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price.id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                # customer_creation='always',
                success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}'+f'&donation_type={donation_type}'+f'&email={email}',
                cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
            )
        # Create a Stripe Price object
        price = stripe.Price.create(
            unit_amount=donation_amount,
            currency="cad",
            product=settings.PRODUCT_ID,  # Ensure you have a product created in Stripe and its ID in settings
        )
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [
                {
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            mode = 'payment',
            customer_creation = 'always',
            success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}'+f'&donation_type={donation_type}'+f'&email={email}',
            cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)
    return render(request, 'getinvolved.html', context)

from .models import UserPayment
## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    donation_type = request.GET.get('donation_type', None)
    email = request.GET.get('email', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    # Create a new UserPayment record
    user_payment = UserPayment.objects.create(
        app_user=email,
        stripe_charge_id=checkout_session_id,
        amount=session.amount_total / 100,  # Convert from cents to dollars
        currency=session.currency,
        donation_type=donation_type
        # success=True,
        
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
                # Create an invoice item
            stripe.InvoiceItem.create(
                customer=stripe.Customer.retrieve(session.customer).id,
                amount=int(user_payment.amount * 100),
                currency='cad',
                description=f"{user_payment.donation_type.capitalize()} Donation",
            )

            # Create and finalize the invoice
            invoice = stripe.Invoice.create(
                customer=stripe.Customer.retrieve(session.customer).id,
                collection_method='send_invoice',  # Auto-finalize this draft after ~1 hour
            )
            # Finalize and send the invoice
            finalized_invoice = stripe.Invoice.finalize_invoice(invoice.id)
            
            # Send the invoice to the customer's email
            stripe.Invoice.send_invoice(finalized_invoice.id)
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