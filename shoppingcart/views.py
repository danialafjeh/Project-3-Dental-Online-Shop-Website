from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product, UserDeliveryInfo
from django.contrib import messages
from django.http import JsonResponse
from .cart import Cart

# Create your views here.

def product_details(request,pk):
    product = Product.objects.get(id=pk)
    suggested_products = Product.objects.all()
    info = {
        'product':product,
        'suggested_prods':suggested_products
    }
    return render(request, 'product_details.html', info)

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total_price = cart.get_total()
    info = {
        'products':cart_products, 
        'quantities':quantities, 
        'total_price':total_price
    }
    return render(request, 'cart_summary.html', info)

def cart_finalcheck(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total_price = cart.get_total()
    user_delivery_info = UserDeliveryInfo.objects.get(user__id=request.user.id)

    required_fields = [
        user_delivery_info.full_name,
        user_delivery_info.phone,
        user_delivery_info.address,
        user_delivery_info.city,
        user_delivery_info.province,
        user_delivery_info.zip_code,
        user_delivery_info.delivery_method
    ]

    if any(field in [None, "", " "] for field in required_fields):
        messages.success(request, ('ابتدا اطلاعات ارسال سفارش خود را در حساب کاربری تان ثبت کنید'))
        return redirect('home')

    info = {
        'products':cart_products,
        'quantities':quantities, 
        'total_price':total_price, 
        'user_delivery':user_delivery_info
    }
    return render(request, 'cart_finalcheck.html', info)

def cart_add(request):
    cart = Cart(request)

    if request.method == 'POST':
        product_id = int(request.POST['product_id'])
        product_qty = int(request.POST['product_qty'])
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        messages.success(request, ("به سبد خرید شما اضافه شد!"))
        return redirect('home')
    else:
        return redirect('home')

def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(request.POST['product_id'])
        cart.delete(product=product_id)
        messages.success(request, ("از سبد خرید شما حذف شد!"))
        return redirect('cart_summary')
    else:
        return redirect('home')
