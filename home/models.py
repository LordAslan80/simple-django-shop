from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug])


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=250)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('home:product_details', args=[self.slug])


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} - {self.created} - {self.body}'