# Generated by Django 5.2.1 on 2025-05-21 15:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Họ và tên đầy đủ')),
                ('phone_number', models.CharField(max_length=20, unique=True, verbose_name='Số điện thoại')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Địa chỉ')),
            ],
            options={
                'verbose_name': 'Khách hàng',
                'verbose_name_plural': 'Khách hàng',
            },
        ),
    ]
