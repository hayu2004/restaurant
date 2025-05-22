from django.db import models
from customer.models import Customer


# Create your models here.

class Table(models.Model):
    floor = models.IntegerField()
    is_used = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    capacity = models.PositiveIntegerField()
    
    def is_available_for(self, number_of_people):
        return not self.is_booked and not self.is_used and self.capacity >= number_of_people
    
    def book(self):
        self.is_booked = True
        self.save()

    def release(self):
        self.is_booked = False
        self.save()
        
    def check_in(self):
        self.is_used = True
        self.save()
        
    def check_out(self):
        self.is_used = False
        self.save()

    def __str__(self):
        return f"Table {self.id} on Floor {self.floor}"
    
class TableBooked(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Đang chờ xử lý'),
        ('confirmed', 'Đã xác nhận'),
        ('cancelled', 'Đã hủy'),
        ('completed', 'Đã hoàn thành'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Khách hàng")
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bàn")
    number_of_guests = models.PositiveIntegerField(verbose_name="Số lượng khách")
    booking_time = models.DateTimeField(verbose_name="Thời gian đặt")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Đặt bàn của {self.user.username} lúc {self.booking_time.strftime('%Y-%m-%d %H:%M')}"
    
