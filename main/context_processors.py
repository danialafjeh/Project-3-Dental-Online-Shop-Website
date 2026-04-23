from .models import Category, Brand
from shoppingcart.cart import Cart

def categories(request):
    all_cats = Category.objects.all()
    info = {'categories':all_cats}
    return info

def brands(request):
    all_brands = Brand.objects.all()
    info = {'brands':all_brands}
    return info

def cart(request):
    return {'cart':Cart(request)}
