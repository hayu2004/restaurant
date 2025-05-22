from django import forms
from .models import Table

class BookingForm(forms.Form):
    full_name = forms.CharField(label="Họ và tên", max_length=255, required=True)
    phone = forms.CharField(label="Số điện thoại", max_length=20, required=True)
    address = forms.CharField(label="Địa chỉ", max_length=255, required=True)

    date = forms.DateField(label="Ngày đặt", widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(label="Giờ đặt", widget=forms.TimeInput(attrs={'type': 'time'}))
    number_of_guests = forms.IntegerField(label='Số lượng người', min_value=1)


class CancelForm(forms.Form):
    customer_id = forms.IntegerField(label="ID Khách hàng")
