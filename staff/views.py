from django.shortcuts import render
from tables.models import *
from tables.forms import *
from menu.models import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from forms import UpdateOrderStatusForm
from django.utils import timezone
import datetime
from tables.models import TableBooked, Table


# Create your views here.
def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('staff_manager_dashboard')
            else:
                return redirect('staff_dashboard')  
        else:
            return render(request, 'login.html', {'error': 'Sai tài khoản hoặc mật khẩu.'})
    return render(request, 'login.html')

# Decorator kiểm tra người dùng là quản lý (siêu người dùng)
def manager_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

@login_required
@manager_required
def staff_manager_dashboard(request):
    total_customers = Customer.objects.count()
    total_orders = FoodOrdered.objects.count()
    total_tables = Table.objects.count()
    available_tables = Table.objects.filter(isBooked=False).count()
    total_revenue = FoodOrdered.objects.filter(status='completed').aggregate(models.Sum('total_amount'))['total_amount__sum'] or 0

    return render(request, 'staff_manager_dashboard.html', {
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_tables': total_tables,
        'available_tables': available_tables,
        'total_revenue': total_revenue,
    })



@staff_member_required
def staff_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")

    booked_list = TableBooked.objects.select_related('customer', 'table').order_by('-booked_at')
    order_list = FoodOrdered.objects.select_related('customer').order_by('-order_time')

    return render(request, 'staff_dashboard.html', {
        'booked_list': booked_list,
        'order_list': order_list,
    })

@staff_member_required
def view_customer_orders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        try:
            order = FoodOrdered.objects.get(id=order_id)
            order.status = new_status
            order.save()
        except FoodOrdered.DoesNotExist:
            pass  # Có thể log lỗi ở đây nếu muốn

    order_list = FoodOrdered.objects.select_related('customer').order_by('-order_time')
    return render(request, 'staff_order_list.html', {
        'order_list': order_list,
        'status_choices': FoodOrdered._meta.get_field('status').choices,
    })

@staff_member_required
def view_booked_tables(request):
    booked_list = TableBooked.objects.select_related('customer', 'table').order_by('-booked_at')
    return render(request, 'staff_booked_list.html', {'booked_list': booked_list})

@staff_member_required
def create_booking_manually(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data['customer']
            table = form.cleaned_data['table']
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            number = form.cleaned_data.get('number_of_guests', 1)

            booking_time = datetime.combine(date, start_time)

            table.book()
            TableBooked.objects.create(
                customer=customer,
                table=table,
                booking_time=booking_time,
                end_time=end_time,
                number_of_guests=number,
                status='confirmed'
            )
            return render(request, 'booking_success.html', {'table': table, 'customer': customer})
    else:
        form = BookingForm()
    
    return render(request, 'book_table.html', {'form': form})
