from django.db import models
from tables.models import Table
from customer.models import Customer

# Create your models here.
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    # Uncomment hàm save này và import slugify nếu bạn muốn slug tự động tạo
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name) # Cần import: from django.utils.text import slugify
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Danh mục món ăn"
        verbose_name_plural = "Các danh mục món ăn"

class Menu(models.Model):
    category = models.ForeignKey(Category, related_name='menu_items', on_delete=models.CASCADE, verbose_name="Danh mục")
    name = models.CharField(max_length=150, verbose_name="Tên món ăn")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá (VNĐ)") # Sửa decimal_places=0
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True, verbose_name="Hình ảnh")
    is_available = models.BooleanField(default=True, verbose_name="Còn hàng")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Món ăn"
        verbose_name_plural = "Thực đơn"
        ordering = ['category', 'name']

    
class FoodOrdered(models.Model):
    ORDER_TYPE_CHOICES = [
        ('dine-in', 'Tại nhà hàng'),
        ('takeaway', 'Mang về'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Đang chờ xử lý'),
        ('preparing', 'Đang chuẩn bị'),
        ('ready', 'Sẵn sàng giao'),
        ('completed', 'Đã hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Đặt bàn liên quan")
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default='dine-in', verbose_name="Loại đơn hàng")
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Tổng tiền (VNĐ)") # Sửa decimal_places=0
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú đơn hàng")

    def __str__(self):
        return f"Đơn hàng #{self.id} của {self.customer}"
    
    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Các đơn hàng"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(FoodOrdered, related_name='items', on_delete=models.CASCADE, verbose_name="Đơn hàng")
    menu_item = models.ForeignKey(Menu, on_delete=models.PROTECT, verbose_name="Món ăn") # PROTECT để tránh xóa món ăn nếu đã có trong đơn hàng
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    price_at_order = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá tại thời điểm đặt (VNĐ)") # Sửa decimal_places=0

    def get_total_item_price(self):
        return self.quantity * self.price_at_order

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} trong ĐH #{self.order.id}"

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Các chi tiết đơn hàng"