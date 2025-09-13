from home.models import Product
from account.models import Profile
from django.shortcuts import get_object_or_404
from .models import Order, OrderItems, Coupon
import datetime


class Cart:
    def __init__(self, request):
        self.user = request.user
        if request.user.profile.active_order:
            self.order = Order.objects.get(id=request.user.profile.active_order, user=request.user, paid=False)
            self.items = self.order.items.all()
    
    def __len__(self):
        return sum(item.quantity for item in self.items)
    
    def get_product(self, product_id):
        product = get_object_or_404(Product, id=product_id)
        return product
    
    def get_order_items(self, product_id):
        product = self.get_product(product_id)
        items = self.items.filter(product=product).first()
        return items
    
    def get_profile(self):
        return Profile.objects.get(user=self.user)
    
    def create_order_items(self, order, product, quantity):
        OrderItems.objects.create(order=order, product=product, price=product.price, quantity=quantity)
    
    def add_product(self, product_id, quantity):
        product = self.get_product(product_id)
        if self.user.profile.active_order is None:
            order = Order.objects.create(user=self.user)
            self.create_order_items(order, product, quantity)
            profile = self.get_profile()
            profile.active_order = order.id
            profile.save()
        else:
            item = self.items.filter(product=product).first()
            if self.user.profile.active_order is None or not item:
                self.create_order_items(self.order, product, quantity)
            elif item:
                item.quantity += quantity
                item.save()

    def remove_product(self, product_id):
        product = self.get_product(product_id)
        self.items.filter(product=product, order=self.order).delete()
    
    def product_plus(self, product_id):
        item = self.get_order_items(product_id)
        item.quantity += 1
        item.save()
    
    def product_minus(self, product_id):
        item = self.get_order_items(product_id)
        if item:
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
    
    def apply_delivery(self, company, price):
        self.order.delivery_company = company
        self.order.delivery_price = price
        self.order.save()
        
    def apply_coupon(self, code):
        now = datetime.datetime.now()
        try:
            coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            self.order.discount = coupon.discount
            self.order.save()
            return True
        except Coupon.DoesNotExist:
            return False
    
    def apply_checkout(self):
        if self.order.delivery_company and self.order.delivery_price:
            self.order.paid = True
            self.order.save()
            profile = self.get_profile()
            profile.active_order = None
            profile.total_paid += self.order.get_products_total()
            profile.total_discount += self.order.get_discount_price()
            profile.order_count += 1
            profile.item_count += self.order.get_products_count()
            profile.save()