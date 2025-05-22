from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Table, TableBooked
from .forms import BookingForm, CancelForm
from customer.models import Customer
from datetime import timedelta, timezone

from datetime import datetime
from django.contrib.auth.decorators import login_required

def table_list(request):
    tables = Table.objects.all()
    return render(request, 'table.html', {'tables': tables})

def update_table_status():
    now = timezone.now()
    booking = TableBooked.objects.filter(status ='confirmed')
    for book in booking:
        if book.booking_time - timedelta(minutes=30) <= now <= book.booking_time:
            if not book.table.is_used():
                book.table.is_used = True
                book.table.save()
                
        elif now > book.booking_time + timedelta(minutes=30):
            if not book.table.is_used():
                book.table.is_booked = False
                book.table.save()
                book.status = 'cancelled'
                book.save()

def table_order(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            number_of_guests = form.cleaned_data['number_of_guests']

            booking_time = datetime.combine(date, start_time)

            # Tạo hoặc cập nhật thông tin khách hàng
            customer, created = Customer.objects.get_or_create(phone_number=phone)
            customer.full_name = full_name
            customer.phone_number = phone
            customer.address = address
            customer.save()

            # Chưa gán bàn cụ thể, staff sẽ xử lý sau
            TableBooked.objects.create(
                customer=customer,
                table=None,  # chưa chọn bàn
                number_of_guests=number_of_guests,
                booking_time=booking_time,
                status='pending'
            )

            return redirect('success')
    else:
        form = BookingForm()

    return render(request, 'form.html', {'form': form})

def success(request):
    return render(request, 'booking_success.html')

def failed(request):
    return render(request, 'booking_failed.html')

def cancel_booking(request):
    if request.method == 'POST':
        form = CancelForm(request.POST)
        if form.is_valid():
            customer_id = form.cleaned_data['Customer_id']
            try:
                customer = Customer.objects.get(id=customer_id)
                booking = TableBooked.objects.filter(customer=customer).first()

                if booking:
                    table = booking.table
                    booking.delete()
                    if table:
                        table.release()
                    return render(request, 'cancel_success.html', {'customer': customer})
                else:
                    return render(request, 'cancel_failed.html', {'reason': 'Không có đặt bàn nào để hủy.'})

            except Customer.DoesNotExist:
                return render(request, 'cancel_failed.html', {'reason': f"ID {customer_id} không tồn tại"})
    else:
        form = CancelForm()

    return render(request, 'cancel_form.html', {'form': form})
