from django.shortcuts import render
from .forms import ContactForm
def home(request):
    return render(request, 'home.html', {'active_page': 'home'})

def about_us(request):
    return render(request, 'aboutus.html', {'active_page': 'about'})

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render('contact_success.html')
    else:
        form = ContactForm()
        return render(request, 'contactus.html', {'active_page': 'contact'})
    
    

def contact_success(request):
    return render(request, 'contact_success.html')
    

def programs(request):
    return render(request, 'programs.html', {'active_page': 'programs'})

def get_involved(request):
    return render(request, 'getinvolved.html', {'active_page': 'getinvolved'})

def events(request):
    return render(request, 'events.html', {'active_page': 'events'})

def login_view(request):
    return render(request, 'login.html', {'active_page': 'login'})

def register_view(request):
    return render(request, 'register.html', {'active_page': 'register'})

def resources_view(request):
    return render(request, 'resources.html', {'active_page': 'resources'})