import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import DetailView, View
from django.contrib.contenttypes.models import ContentType
from .mixins import CartMixin
from .models import Pizza, Sushi, Customer, CartProduct
from .forms import OrderForm
from django.contrib import messages


class BaseView(CartMixin, View):
    def get(self, request):
        context = {
            'cart': self.cart
        }
        return render(request, 'main/index.html', context)


def pizza(request):
    pizza_qs = Pizza.objects.all()
    context = {
        'products': pizza_qs
    }
    return render(request, 'main/pizza.html', context)


def sushi(request):
    sushi_qs = Sushi.objects.all()
    context = {
        'products': sushi_qs
    }
    return render(request, 'main/sushi.html', context)


class ProductDetailView(CartMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'pizza': Pizza,
        'sushi': Sushi
    }
    context_object_name = 'product'
    template_name = 'main/product_detail.html'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart
        }
        return render(request, 'main/cart.html', context)


class CheckoutView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart, 
            'form' : form
        }
        return render(request, 'main/checkout.html', context)


class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        ct_model = kwargs.get('ct_model')
        product_slug = kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id)
        cart_product.delete()
        return HttpResponseRedirect('/cart/')


class MakeOrderView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.cart = self.cart
            self.cart.in_order = True
            self.cart.save()
            new_order.save()
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class UpdateCartProductAmountView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        ct_model = kwargs.get('ct_model')
        product_slug = kwargs.get('slug')
        new_amount = kwargs.get('new_amount')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id)
        cart_product.qty = new_amount 
        cart_product.save()

        response = json.dumps({
            'status': 'ok',
            'item_final_price': float(cart_product.final_price),
            'final_price': float(self.cart.final_price)
        })
        return JsonResponse(response, safe=False)
