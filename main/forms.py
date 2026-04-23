from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from .models import UserDeliveryInfo
from django import forms

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="نام ",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control font-weight-bold border-primary border-2'})
    )
    last_name = forms.CharField(
        label="نام خانوادگی ",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control font-weight-bold border-primary border-2'})
    )
    email = forms.EmailField(
        label="ایمیل ",
        widget=forms.TextInput(attrs={'type':'email', 'class':'form-control font-weight-bold border-primary border-2'})
    )
    username = forms.CharField(
        label="نام کاربری ",
        max_length=20,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control font-weight-bold border-primary border-2'})
    )
    password1 = forms.CharField(
        label="رمز عبور بالای 8 کاراکتر خود را وارد کنید ",
        widget=forms.PasswordInput(
        attrs={
            'class':'form-control font-weight-bold border-primary border-2',
            'name':'password',
            'type':'password',
        }
        )
    )
    password2 = forms.CharField(
        label="رمز عبور خود را دوباره وارد کنید ",
        widget=forms.PasswordInput(
        attrs={
            'class':'form-control font-weight-bold border-primary border-2',
            'name':'password',
            'type':'password',
        }
        )
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        )
        

class UserDeliveryInfoForm(forms.ModelForm):
    full_name = forms.CharField(
        label="نام کامل ",
        widget=forms.TextInput(attrs={'class':'form-control font-weight-bold border-primary border-2', 'type':'text'}),
        required=True

    )
    phone = forms.CharField(
        label="شماره تماس ",
        widget=forms.TextInput(attrs={'class':'form-control font-weight-bold border-primary border-2', 'type':'text'}),
        required=True

    )
    address = forms.CharField(
        label="آدرس ",
        widget=forms.TextInput(attrs={'class':'form-control font-weight-bold border-primary border-2', 'type':'textarea'}),
        required=True

    )
    city = forms.CharField(
        label="شهر ",
        widget=forms.TextInput(attrs={'class':'form-control font-weight-bold border-primary border-2', 'type':'text'}),
        required=False

    )
    province = forms.CharField(
        label="استان ",
        widget=forms.TextInput(attrs={'class':'form-control font-weight-bold border-primary border-2', 'type':'text'}),
        required=False

    )
    zip_code = forms.CharField(
        label="کد پستی ",
        widget=forms.TextInput(attrs={'class':'form-control font-weight-bold border-primary border-2', 'type':'text'}),
        required=True

    )
    
    DELIVERY_CHOICES = [
        ('post', 'ارسال با پست'),
        ('peyk', 'ارسال با پیک'),
    ]
    delivery_method = forms.ChoiceField(
        label="نحوه ارسال ",
        choices=DELIVERY_CHOICES,
        widget=forms.Select(attrs={'class':'form-select font-weight-bold border-primary border-2'}),
        required=True
    )

    class Meta:
        model = UserDeliveryInfo
        fields = (
            'full_name',
            'phone',
            'province',
            'city',
            'address',
            'zip_code',
            'delivery_method' 
        ) 

class UpdateUserForm(UserChangeForm):
    password = None

    first_name = forms.CharField(
        label="نام ",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control font-weight-bold border-primary border-2'})
    )
    last_name = forms.CharField(
        label="نام خانوادگی ",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control font-weight-bold border-primary border-2'})
    )
    username = forms.CharField(
        label="نام کاربری ",
        max_length=20,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control font-weight-bold border-primary border-2'})
    )
    email = forms.EmailField(
        label="ایمیل ",
        widget=forms.TextInput(attrs={'type':'email', 'class':'form-control font-weight-bold border-primary border-2'})
    )

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')

class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="رمز جدید خود را وارد کنید",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control font-weight-bold border-primary border-2',
                'name':'password',
                'type':'password'
            }
        )
    )
    new_password2 = forms.CharField(
        label="رمز خود را دوباره وارد کنید ",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control font-weight-bold border-primary border-2',
                'name':'password',
                'type':'password'
            }
        )
    )

    class Meta:
        model = User
        fields = ('new_password1','new_password2')
