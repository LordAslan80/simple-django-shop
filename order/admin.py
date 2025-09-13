from django.contrib import admin
from .models import Order, OrderItems, Coupon, DeliveryOptions


class OrderItemInline(admin.TabularInline):
    model = OrderItems
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'discount']
    list_filter = ['created', 'delivery_company']
    inlines = [OrderItemInline]


admin.site.register(Coupon)
admin.site.register(DeliveryOptions)