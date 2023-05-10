from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update date')

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField()
    discount_percent = models.DecimalField(max_digits=12, decimal_places=6)
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update date')


class Product(models.Model):

    class Sizes(models.TextChoices):
        L = 'L', 'Large'
        M = 'M', 'Medium'
        S = 'S', 'Small'

    class Color(models.TextChoices):
        Red = 'red', 'RED'
        Green = 'green', 'GREEN'
        White = 'white', 'WHITE'       

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=6, choices=Color.choices, null=True, blank=True)
    size = models.CharField(max_length=10, choices=Sizes.choices, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', null=True, on_delete=models.SET_NULL)
    inventory = models.IntegerField()
    discount = models.ForeignKey(Discount, related_name='products', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update date')

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, related_name='carts', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update date')
    total = models.IntegerField(null=True, blank=True, default = 0)
    is_active = models.BooleanField(default=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=12, decimal_places=6, default=1, null=True)


class Order(models.Model):
    user = models.ForeignKey(User, null=True, related_name='orders', on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=6, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')