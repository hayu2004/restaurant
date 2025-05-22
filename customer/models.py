from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Customer(models.Model):
    Customer_id = models.AutoField(primary_key=True, verbose_name="Mã khách hàng")
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Họ và tên đầy đủ")
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="Số điện thoại")
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")

    def __str__(self):
        return self.full_name or self.phone_number or f"Khách hàng #{self.id}"
    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"
    