from django.db import models
from django.contrib.auth import get_user_model
from home.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
import jdatetime


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(blank=True, null=True, default=0)
    delivery_company = models.CharField(max_length=150, blank=True, null=True,)
    delivery_price = models.IntegerField(blank=True, null=True,)
    
    class Meta:
        ordering = ['paid', '-updated']
    
    def __str__(self) -> str:
        return f'{self.user} - {self.id}'
    
    def get_products_total(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_discount_price(self):
        return int((self.discount / 100) * self.get_products_total()) if self.discount else 0
    
    def get_total_price(self):
        total = self.get_products_total()
        if self.discount:
            total = int(total - self.get_discount_price())
        if self.delivery_price:
            total = (total + self.delivery_price)
        return total
    
    def get_products_count(self):
        return sum(item.quantity for item in self.items.all())
    
    def get_persian_datetime(self):
        return jdatetime.datetime.fromgregorian(datetime=self.updated)
    
    def get_products_data(self):
        return self.items.all()
        

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return self.id
    
    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.code


class DeliveryOptions(models.Model):
    company_name = models.CharField(max_length=150)
    price = models.IntegerField()
    
    class Meta:
        verbose_name = 'delivery Options'
        verbose_name_plural = 'delivery Options'
    
    def __str__(self) -> str:
        return f'{self.company_name} - {self.price}'