"""
URL configuration for Fgen_New project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from new_App import views
from django.conf.urls import handler404

handler404 = "new_App.views.custom_page_not_found_view"

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('programs/', views.programs, name='programs'),
    path('involved/', views.getinvolved_page, name='get_involved'),
    path('events/', views.events, name='events'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('contact_success/', views.contact_success, name='contact_success'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    # path('getinvolved_page/', views.getinvolved_page, name='getinvolved_page'),
	path('payment_successful', views.payment_successful, name='payment_successful'),
	path('payment_cancelled', views.payment_cancelled, name='payment_cancelled'),
	path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
    path('events/create/', views.create_event, name='create_event'),
]
