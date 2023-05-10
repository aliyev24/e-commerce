from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from . import services
from . import views
from . import models
from . import serializers


class TestRynok(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuserr', password='12345')
        self.client.force_login(user=self.user)

        models.Category.objects.create(
            name='Computers',
            description='Intel',
            created_at='2022-07-31T08:05:27.205132Z',
            updated_at='2022-07-31T08:05:27.205132Z'
        )

        self.product1 = models.Product.objects.create(
            name='Lenovo',
            description='New generation',
            created_at='2022-07-31T08:05:27.205132Z',
            updated_at='2022-07-31T08:05:27.205132Z',
            price=100,

            inventory=5550

        )

        self.product2 = models.Product.objects.create(
            name='qrafin',
            description='New generation',
            created_at='2022-07-31T08:05:27.205132Z',
            updated_at='2022-07-31T08:05:27.205132Z',
            price=255,
            inventory=8
        )

        models.CartItem.objects.create(
            product=models.Product.objects.get(name='qrafin'),
            quantity=1,
            cart=models.Cart.objects.get(user=self.user),
            is_active=True,
            cost = 3
            
        )

        models.Order.objects.create(
            user = self.user,
            cart = models.Cart.objects.get(user=self.user),
            total = 0
        )

    def test_product_list(self):
        response = self.client.get(reverse('product_list'))        
        expectedData = serializers.ProductSerializer(models.Product.objects.all(),many = True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,expectedData.data)


    def test_product_detail(self):
        response = self.client.get(reverse('product_detail',kwargs={'pk': self.product1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Lenovo')

    
    def test_cartitem_new(self):
        data = {
            'product': 1,
            'quantity': 5,
            'cart': 1,
            'cost': 10
        }
        url = reverse('cart_item_new')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_carts(self):
        response=self.client.get(reverse('carts'))
        expectedData = serializers.CartSerializer(models.Cart.objects.filter(is_active=True,user=self.user), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expectedData.data)
        

    def test_cartitem_view(self):
        response = self.client.get(reverse('cartitems'))
        cart = models.Cart.objects.get(user=self.user, is_active=True)
        expectedData = serializers.CartItemSerializer(models.CartItem.objects.filter(cart=cart),many = True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expectedData.data)
        

    def test_order_list(self):
        response = self.client.get(reverse('order_list'))
        expectedData = serializers.OrderSerializer(models.Order.objects.filter(user=self.user),many = True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,expectedData.data)


    def test_minus_inventory(self):
        self.product3 = models.Product.objects.create(
            name='Boots',
            description='News generation',
            created_at='2022-07-31T08:05:27.205132Z',
            updated_at='2022-07-31T08:05:27.205132Z',
            price=255,
            inventory=100
        )
        data = {
            'product': self.product3.id,
            'quantity': 5,
            'is_active' : True,
            'cart': 1,
            'cost': 10
        }
        serializer = serializers.CartItemSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            services.minus_inventory(serializer)
            
        self.assertEqual(models.Product.objects.get(name='Boots').inventory, 95)

    def test_total_cart(self):
        data = {

            'product': self.product1.id,
            'quantity': 1
            }
        serializer = serializers.CartItemSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            
            services.total_cart(self.user,serializer)
        self.assertEqual(models.Cart.objects.get(user=self.user).total, 100.0)