from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return f'دسته بندی : {self.name}'

class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=10000, blank=True)

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"

    def __str__(self):
        return f'{self.name} : برند'

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=10000, blank=True)
    extra_description = models.TextField(max_length=10000, blank=True)
    picture = models.ImageField(upload_to='upload/products/')
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return f'محصول : {self.name}'
    
class UserDeliveryInfo(models.Model):
    DELIVERY_CHOICES = [
        ('post', 'ارسال با پست'),
        ('peyk', 'ارسال با پیک'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=25, blank=True)
    address = models.TextField(max_length=500, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, null=True)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, null=True)
    shopping_cart = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "مشخصات ارسال سفارش مشتری"
        verbose_name_plural = "مشخضات ارسال سفارش مشتریان"

    def __str__(self):
        return f'Delivery Info - {self.user.username}'

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserDeliveryInfo(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

class ShopInfo(models.Model):
    shop_address = models.TextField(max_length=1000)

    shop_email_1 = models.EmailField(max_length=100)
    shop_email_2 = models.EmailField(max_length=100, blank=True)

    shop_phone_1 = models.CharField(max_length=25)
    shop_phone_2 = models.CharField(max_length=25, blank=True) 
    shop_phone_3 = models.CharField(max_length=25, blank=True)

    class Meta:
        verbose_name = "اطلاعات فروشگاه"
        verbose_name_plural = "اطلاعات فروشگاه"

    def __str__(self):
        return f'اطلاعات فروشگاه'
    

    

    



    
