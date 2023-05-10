from . import models


def minus_inventory(serializer):
    """
    After User adds product to the Cart, service minuses amount of product from inventory.
    """
    product = models.Product.objects.get(id=serializer.validated_data['product'].id)
    if product.inventory >= 0:
        product.inventory -= serializer.validated_data['quantity']
        product.save()


def total_cart(user,serializer):
    """
    Calculates total cost of the Cart, after product added to it.
    """
    cart = models.Cart.objects.get(user=user,is_active=True)
    product = models.Product.objects.get(id=serializer.validated_data['product'].id)
    sum = 0
    sum += product.price*serializer.validated_data['quantity']
    cart.total += sum
    cart.save()


def create_cart(user):
    """
    After payment completed for the Cart, service creates new cart.
    The previous cart becomes not active.
    """
    cart = models.Cart.objects.get(user=user, is_active=True)
    cart.is_active = False
    cart.save()
    models.Cart.objects.create(user=user)


def sum_order(user,serializer):
    """
    Sums all the products' costs in the Cart.
    """
    cart = models.Cart.objects.get(user=user,is_active=True)
    order= models.Order.objects.get(id=serializer.data['id'])
    order.total = cart.total
    order.save()

