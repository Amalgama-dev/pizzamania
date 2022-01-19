import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import DetailView, View
from django.contrib.contenttypes.models import ContentType
from .mixins import CartMixin
from .models import Pizza, Sushi, Category, LatestProducts, Customer, Cart, CartProduct
from .forms import OrderForm
from django.contrib import messages



class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
       
        context = {
            
            'cart': self.cart
        }
        return render(request, 'main/index.html', context)


def pizza(request):
    pizza_qs = Pizza.objects.all()
    return render(request, 'main/pizza.html', {'products': pizza_qs})



def sushi(request):
    sushi_qs = Sushi.objects.all()
    return render(request, 'main/sushi.html', {'products': sushi_qs})


class ProductDetailView(CartMixin, DetailView):

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
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        if created:
            self.cart.products.add(cart_product)
        self.cart.final_price += (cart_product.final_price)
        self.cart.save()
        return HttpResponseRedirect('/cart/')



class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model = kwargs.get('ct_model')
        product_slug = kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id)
        
        self.cart.products.remove(cart_product)
        self.cart.final_price -= (cart_product.final_price)
        cart_product.delete()
        self.cart.save()
        return HttpResponseRedirect('/cart/')


class ChangeQTYVIEW(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id)
        
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        self.cart.save()
        return HttpResponseRedirect('/cart/')


class MakeOrderView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
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
        old_price = cart_product.final_price
        cart_product.qty = new_amount 
        new_price = cart_product.final_price = new_amount * product.price
        cart_product.save()
        self.cart.final_price += new_price - old_price
        self.cart.save()

        response = json.dumps({
            'status': 'ok',
            'item_final_price': float(new_price),
            'final_price': float(self.cart.final_price)
        })
        return JsonResponse(response, safe=False)
