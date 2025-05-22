# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Customer

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text="Yêu cầu. 150 ký tự hoặc ít hơn. Chỉ chữ cái, số và @/./+/-/_.")
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Xác nhận mật khẩu")

    # Các trường cho model Customer (lưu ý: các trường này không phải của User model)
    full_name = forms.CharField(max_length=255, required=False, label="Họ và tên đầy đủ")
    phone_number = forms.CharField(max_length=20, label="Số điện thoại")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Địa chỉ")

    class Meta:
        model = User # Form này sẽ thao tác chính với User
        fields = ['username', 'email', 'password'] # Các trường User cơ bản

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tên đăng nhập này đã tồn tại. Vui lòng chọn tên khác.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Địa chỉ email này đã được sử dụng. Vui lòng chọn email khác.")
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Mật khẩu không khớp.")
        return confirm_password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Customer.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Số điện thoại này đã được đăng ký.")
        # Bạn có thể thêm các kiểm tra định dạng số điện thoại ở đây nếu cần
        return phone_number

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        # Nếu có first_name, last_name từ full_name (tùy chọn xử lý)
        # user.first_name = ...
        # user.last_name = ...
        if commit:
            user.save()

        customer = Customer(
            user=user,
            full_name=self.cleaned_data.get('full_name'),
            phone_number=self.cleaned_data['phone_number'],
            address=self.cleaned_data.get('address')
        )
        if commit:
            customer.save()
        return user, customer


class CustomerLoginForm(forms.Form):
    username = forms.CharField(label="Tên đăng nhập hoặc Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")