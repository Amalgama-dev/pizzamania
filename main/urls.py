from django.urls import path, include
from main import views

urlpatterns = [
    path('', views.BaseView.as_view(), name='main'),
    path('pizza', views.pizza, name='pizza'),
    path('sushi', views.sushi, name='sushi'),
    path('products/<str:ct_model>/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', views.DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('update-cart-product-amount/<str:ct_model>/<str:slug>/<int:new_amount>', views.UpdateCartProductAmountView.as_view(), name='update-cart-product-amount'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('make-order/', views.MakeOrderView.as_view(), name='make_order')
]

