from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets,status,filters
from django_filters import rest_framework as rest_filters, CharFilter, NumberFilter
from django.http import JsonResponse
import json

from . import models
from . import services
from . import serializers


class ProductFilter(rest_filters.FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr='gte')
    max_price = NumberFilter(field_name="price", lookup_expr='lte')
    category = CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = models.Product
        fields = ['category', ]


def store(request):
	carts = models.Cart.objects.filter(is_active=True,user=request.user)
	context = {'carts':carts}
	return render(request, 'market/store.html', context)


def simpleCheckout(request):
	return render(request, 'market/simple_checkout.html')


def checkout(request, pk):
	carts = models.Cart.objects.get(id=pk)
	context = {'cart':carts}
	return render(request, 'market/checkout.html', context)


def paymentComplete(request):
    body = json.loads(request.body)
    order = models.Order.objects.create(
        user = request.user,
        cart = models.Cart.objects.get(user=request.user, is_active=True))
    serializer = serializers.OrderSerializer(order)
    services.sum_order(request.user,serializer)
    services.create_cart(request.user)
    return JsonResponse('Payment completed!', safe=False)


class HomeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['color', 'size']


class AddCartItem(APIView):

    def post(self,request):
        """
        Adds product as cart item to User's cart.
        """
        serializer = serializers.CartItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            cart = models.Cart.objects.get(user=request.user,is_active=True)
            serializer.save(cart=cart)
            services.minus_inventory(serializer)
            services.total_cart(request.user, serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        return models.Cart.objects.filter(user=self.request.user,is_active=True)


class CartItemViewSet(ModelViewSet):
    serializer_class = serializers.CartItemSerializer

    def get_queryset(self):
        cart = models.Cart.objects.get(user=self.request.user, is_active=True)
        return models.CartItem.objects.filter(cart=cart)


class OrderViewSet(ModelViewSet):
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user)