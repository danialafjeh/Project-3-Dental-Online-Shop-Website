from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
import json
from shoppingcart.cart import Cart
from django.contrib.auth.models import User
from .forms import SignUpForm, UserDeliveryInfoForm, UpdateUserForm, UpdatePasswordForm
from .models import Category, Product, Brand, UserDeliveryInfo, ShopInfo
from payment.models import Order

# Create your views here.

def home(request):
    sale_prods = Product.objects.filter(is_sale=True)
    info = {'sale_products':sale_prods}
    return render(request, 'home.html', info)

def products(request):
    prods = Product.objects.all()
    info = {'products':prods}
    return render(request, 'products.html', info)

def products_category(request, cat):
    cat = cat.replace("-"," ")
    category = Category.objects.get(name=cat)
    products = Product.objects.filter(category=category)
    info = {
        'category':category, 
        'products':products
    }
    return render(request, 'category.html', info)

def products_brand(request, brand):
    brand_name = brand.replace("-"," ")
    brand = Brand.objects.get(name=brand_name)
    products = Product.objects.filter(brand=brand)
    info = {
        'brand':brand, 
        'products':products
    }
    return render(request, 'brand.html', info)


def contactus(request):
    shop_information = ShopInfo.objects.get(id=1)
    return render(request, 'contact.html', {'shopinfo':shop_information})

TRANSLATE_ERRORS = {
    "This field is required.": "این فیلد ضروری است.",
    "A user with that username already exists.": "این نام کاربری قبلاً ثبت شده است.",
    "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.":
        "نام کاربری نامعتبر است. فقط حروف، اعداد و کاراکترهای @ . + - _ مجاز هستند.",
    "The two password fields didn’t match.": "رمز عبور و تکرار آن یکسان نیستند.",
    "This password is too short. It must contain at least 8 characters.":
        "رمز عبور خیلی کوتاه است. باید حداقل ۸ کاراکتر باشد.",
    "This password is too common.": "این رمز عبور خیلی معمولی و قابل حدس است.",
    "This password is entirely numeric.": "رمز عبور نباید فقط از اعداد تشکیل شده باشد.",
    "The password is too similar to the username.":
        "رمز عبور بیش از حد شبیه نام کاربری است.",
    "The password is too similar to your first name.":
        "رمز عبور بیش از حد شبیه نام کوچک شماست.",
    "The password is too similar to your last name.":
        "رمز عبور بیش از حد شبیه نام خانوادگی شماست.",
    "The password is too similar to your email address.":
        "رمز عبور بیش از حد شبیه ایمیل شماست.",
    "Enter a valid value.": "مقدار وارد شده معتبر نیست.",
}

def signup_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            messages.success(request,("حساب کاربری شما با موفقیت ساخته شد!"))
            return redirect('user_delivery_info')
        else:
            for field, errors in form.errors.items():
               for error in errors:
                  fa_error = TRANSLATE_ERRORS.get(error, error)
                  messages.error(request, fa_error)

               return redirect('signup')
    else:
        return render(request, 'signup.html',{'form':form})

def login_page(request):
    return render(request, 'login_page.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_staff:
                login(request, user)
                current_user = UserDeliveryInfo.objects.get(user__id = request.user.id)
                saved_cart = current_user.shopping_cart
                if saved_cart:
                   converted_cart = json.loads(saved_cart)
                   cart = Cart(request)

                   for k,v in converted_cart.items():
                       cart.db_add(product=k , quantity=v)
            
                messages.success(request,('با موفقیت وارد حساب کاربری خود شدید!'))
                return redirect('home')
            else:
                messages.success(request, ('حساب مورد نظر حساب مدیریت است. لطفا از بخش ورود مدیران وارد شوید.'))
                return redirect('home')
        else:
            messages.success(request, ('نام کاربری یا رمز عبور اشتباه است.'))
            return redirect('login_user')
    else:
        return render(request, 'login_user.html')
    
def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                current_user = UserDeliveryInfo.objects.get(user__id = request.user.id)
                saved_cart = current_user.shopping_cart
                if saved_cart:
                   converted_cart = json.loads(saved_cart)
                   cart = Cart(request)

                   for k,v in converted_cart.items():
                       cart.db_add(product=k , quantity=v)
            
                messages.success(request,('با موفقیت وارد حساب مدیریت خود شدید!'))
                return redirect('home')
            else:
                messages.success(request, ('شما دسترسی به پنل مدیریت ندارید. لطفا از بخش ورود مشتریان وارد شوید.'))
                return redirect('home')
        else:
            messages.success(request, ('نام کاربری یا رمز عبور اشتباه است.'))
            return redirect('login_admin')
    else:
        return render(request, 'login_admin.html')
    
def logout_account(request):
    logout(request)
    messages.success(request, ('با موفقیت از حساب خود خارج شدید!'))
    return redirect('home')

def deliveryinfomation_user(request):
    if request.user.is_authenticated:
        current_user = UserDeliveryInfo.objects.get(user__id=request.user.id)
        form_delivery = UserDeliveryInfoForm(instance=current_user)
        if request.method == 'POST':
            form_delivery = UserDeliveryInfoForm(request.POST, instance=current_user)
            if form_delivery.is_valid():
                form_delivery.save()
                messages.success(request, ('مشخصات ارسال سفارش برای حساب شما ثبت شد!'))
                return redirect('home')
            else:
                messages.success(request,("مشکلی در ثبت اطلاعات وجود داشت!"))
                return redirect('user_delivery_info')
        else:
            return render(request, 'userdeliveryinfo.html', {'form_delivery':form_delivery})
    else:
        messages.success(request,('ابتدا باید وارد حساب کاربری خود شوید!'))
        return redirect('home')

def profile_user(request):
    if request.user.is_authenticated:
        user_account_info = User.objects.get(id=request.user.id)
        user_delivery_info = UserDeliveryInfo.objects.get(user__id=request.user.id)

        active_orders = Order.objects.filter(user__id = request.user.id).exclude(status__in=['canceled','Delivered'])
        canceled_orders = Order.objects.filter(user__id = request.user.id, status='canceled')
        delivered_orders = Order.objects.filter(user__id = request.user.id, status='Delivered')
        info = {
           'user_account':user_account_info ,
           'user_delivery':user_delivery_info,
           'active_orders':active_orders , 
           'canceled_orders':canceled_orders, 
           'delivered_orders':delivered_orders
        }
        return render(request, 'profile_user.html', info)
    else:
        messages.success(request,('ابتدا باید وارد حساب کاربری خود شوید!'))
        return redirect('home')

def update_profile(request):
    if request.user.is_authenticated:
       current_user = User.objects.get(id=request.user.id)
       form = UpdateUserForm(instance = current_user)
       if request.method == 'POST':
           form = UpdateUserForm(request.POST, instance = current_user)
           if form.is_valid():
               form.save()
               
               messages.success(request, ('اطلاعات حساب شما ویرایش شد!'))
               return redirect('profile_user')
           else:
               messages.success(request,("مشکلی در ویرایش اطلاعات وجود داشت!"))
               return redirect('update_profile')
       else:
           return render(request, 'update_profile.html', {'form':form})
    else:
        messages.success(request,('ابتدا باید وارد حساب کاربری خود شوید!'))
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        form_pass = UpdatePasswordForm(current_user)
        if request.method =='POST':
            form_pass = UpdatePasswordForm(current_user, request.POST)
            if form_pass.is_valid():
                form_pass.save()
                messages.success(request,('رمز شما با موفقیت ویرایش شد!'))
                login(request, current_user)
                return redirect('profile_user')
            else:
                messages.success(request,('مشکلی در ویرایش رمز عبور حساب شما وجود داشت!'))
                return redirect('update_password')
        else:
            return render(request,'update_password.html',{'form_pass':form_pass})
    else:
        messages.success(request,('ابتدا باید وارد حساب کاربری خود شوید!'))
        return redirect('home')

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) or Q(brand__name__icontains=searched))
        if not searched:
            messages.success(request, ('محصولی با این نام یافت نشد!'))
            return redirect('home')
        else:
            return render(request, 'search_products.html', {'searched':searched})
    else:
        return redirect('home')
