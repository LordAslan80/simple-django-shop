from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from .cart import Cart
from .forms import CouponApplyForm, AddToCardForm
from .models import DeliveryOptions, Order, OrderItems
from django.contrib.auth.mixins import LoginRequiredMixin


class CartView(LoginRequiredMixin, View):
    form_class = CouponApplyForm
    
    def get(self, request):
        delivery = DeliveryOptions.objects.all()
        if request.user.profile.active_order:
            order = get_object_or_404(Order, id=request.user.profile.active_order)
            cart = get_list_or_404(OrderItems, order=order)
            return render(request, 'order/cart.html', {'user':request.user, 'delivery':delivery, 'form':self.form_class, 'cart':cart, 'order':order})
        return render(request, 'order/cart.html', {'user':request.user, 'delivery':delivery, 'form':self.form_class})


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        form = AddToCardForm(request.POST)
        if form.is_valid():
            Cart(request).add_product(product_id, form.cleaned_data['quantity'])
            return redirect('order:cart')
    
    
class CartRemoveView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        Cart(request).remove_product(product_id)
        return redirect('order:cart')


class CartProductPlusView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        Cart(request).product_plus(product_id)
        return redirect('order:cart')


class CartProductMinusView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        Cart(request).product_minus(product_id)
        return redirect('order:cart')


class DeliveryApplyView(LoginRequiredMixin, View):
    def get(self, request, delivery_id):
        if request.user.profile.active_order:
            delivery = DeliveryOptions.objects.get(id=delivery_id)
            Cart(request).apply_delivery(delivery.company_name, delivery.price)
        return redirect('order:cart')


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm
    
    def post(self, request):
        if request.user.profile.active_order:
            form = self.form_class(request.POST)
            if form.is_valid():
                code = form.cleaned_data['code']
                Cart(request).apply_coupon(code)
        return redirect('order:cart')


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        Cart(request).apply_checkout()
        return redirect('order:cart')


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        return render(request, 'order/order_detail.html', {'order':order})