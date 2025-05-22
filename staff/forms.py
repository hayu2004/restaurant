from menu.models import FoodOrdered
from django import forms
from tables.models import Table

class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = FoodOrdered
        fields = ['status']
        
class AssignTableForm(forms.Form):
    booking_id = forms.IntegerField(widget=forms.HiddenInput())
    table = forms.ModelChoiceField(queryset=Table.objects.filter(isBooked=False, isUsed=False), label='Chọn bàn')