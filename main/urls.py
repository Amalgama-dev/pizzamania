from django.urls import path, include
from . import views
from .views import ProductDetailView, CartView, AddToCartView, BaseView, DeleteFromCartView, ChangeQTYVIEW, UpdateCartProductAmountView, CheckoutView, MakeOrderView

urlpatterns = [
    path('', BaseView.as_view(), name='main'),
    path('pizza', views.pizza, name='pizza'),
    path('sushi', views.sushi, name='sushi'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('update-cart-product-amount/<str:ct_model>/<str:slug>/<int:new_amount>', UpdateCartProductAmountView.as_view(), name='update-cart-product-amount'),
    path('change-qty/<str:ct_model>/<str:slug>/', ChangeQTYVIEW.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order')
]

