from django.urls import path
from . import views

urlpatterns =[
    path('product_details/<int:pk>', views.product_details, name='product_details'),
    path('', views.cart_summary, name='cart_summary'),
    path('finalcheck/', views.cart_finalcheck, name='cart_finalcheck'),
    path('add/', views.cart_add, name='cart_add'),
    path('delete/', views.cart_delete, name='cart_delete')
]