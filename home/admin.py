from django.contrib import admin
from .models import Category, Product, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['name']}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['name', 'description']}
    raw_id_fields = ['category']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created', 'is_reply']
    raw_id_fields = ['user', 'product', 'reply']