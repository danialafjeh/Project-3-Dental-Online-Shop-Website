from django.urls import path
from main import views

urlpatterns =[
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('category/<str:cat>', views.products_category, name='category'),
    path('brand/<str:brand>', views.products_brand, name='brand'),
    path('contactus/', views.contactus, name='contactus'),
    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_page, name='login_page'),
    path('login_user/', views.login_user, name='login_user'),
    path('login_admin/', views.login_admin, name='login_admin'),
    path('logout/', views.logout_account, name='logout'),
    path('userdeliveryinfo/', views.deliveryinfomation_user, name='user_delivery_info'),
    path('profile_user/', views.profile_user, name='profile_user'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_password/', views.update_password, name='update_password'),
    path('search/', views.search, name='search_products')
]
