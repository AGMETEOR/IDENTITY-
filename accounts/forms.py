from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':"w3-input"}))
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','first_name','email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('Passwords dont match')
        return cd['password2']

class ExtraDataEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number','location')
    
