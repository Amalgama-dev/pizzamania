from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Pizza, Sushi, Category, LatestProducts, Customer, Cart, CartProduct


def index(request):
    return render(request, 'main/index.html')


def pizza(request):
    pizza_qs = Pizza.objects.all()
    return render(request, 'main/pizza.html', {'products': pizza_qs})


def sushi(request):
    sushi_qs = Sushi.objects.all()
    return render(request, 'main/sushi.html', {'products': sushi_qs})


class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'pizza': Pizza,
        'sushi': Sushi
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'main/product_detail.html'
    slug_url_kwarg = 'slug'

