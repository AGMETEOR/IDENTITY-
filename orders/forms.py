from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['username','firstname','email','phone_number','location']
        widgets = {'username':forms.HiddenInput(),'firstname':forms.HiddenInput(),'email':forms.HiddenInput()}
