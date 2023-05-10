from django.contrib import admin
from . import models


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('is_active','id','user')
    list_display_links = ('is_active','id', 'user')

    
@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('is_active','id','cart')
    list_display_links = ('is_active','id', 'cart')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','id','inventory')
    list_display_links = ('name','id','inventory')


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','cart','total')
    list_display_links = ('id', 'user')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass