from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class StaffManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username là bắt buộc")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Tự động hash mật khẩu
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(username, password, **extra_fields)

class Staff(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [('M', 'Nam'), ('F', 'Nữ'), ('O', 'Khác')]

    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = StaffManager()

    USERNAME_FIELD = 'username'  # Trường đăng nhập
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"