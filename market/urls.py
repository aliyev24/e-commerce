from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from market import views


router = routers.SimpleRouter()

urlpatterns = [
    path('', views.store, name="store"),
    path('checkout/<int:pk>/', views.checkout, name="checkout"),
    path('complete/', views.paymentComplete, name="complete"),
    path('simple-checkout/', views.simpleCheckout, name="simple-checkout"),

    path('products/', views.HomeViewSet.as_view({'get': 'list'}),name ='product_list'),
    path('products/<int:pk>/', views.HomeViewSet.as_view({'get': 'retrieve'}), name='product_detail'),
    
    path('cartitems/', views.CartItemViewSet.as_view({'get': 'list'}), name= 'cartitems'),
    path('cartitems/<int:pk>/', views.CartItemViewSet.as_view({'get': 'retrieve','delete':'destroy','put':'update'})),
    path('cartitem/new/', views.AddCartItem.as_view(), name='cart_item_new'),

    path('carts/', views.CartViewSet.as_view({'get': 'list'}), name='carts'),

    path('orders/', views.OrderViewSet.as_view({'get': 'list'}), name = 'order_list'),
    path('orders/<int:pk>/', views.OrderViewSet.as_view({'get': 'retrieve','delete':'destroy'})),
   
    path('api/v1/drf_auth', include('rest_framework.urls')),
]

urlpatterns += router.urls