# booking/forms.py
from django import forms

class OrderForm(forms.Form):
    food = forms.CharField(label="Food")
    quantity = forms.IntegerField(label="quantity")
    
