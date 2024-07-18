from django import forms
from .models import ContactMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        
class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('phone_number', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('password', css_class='form-control'),
            Field('confirm_password', css_class='form-control'),
            Submit('submit', 'Register', css_class='btn btn-primary')
        )