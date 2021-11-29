from django.urls import path, include
from . import views
from .views import ProductDetailView

urlpatterns = [
    path('', views.index, name='main'),
    path('pizza', views.pizza, name='pizza'),
    path('sushi', views.sushi, name='sushi'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
