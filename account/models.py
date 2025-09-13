from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250, default='خالی')
    phone = models.CharField(max_length=11, default='خالی')
    address = models.TextField(default='خالی')
    image = models.ImageField(upload_to='avatar/', default='avatar.png')
    total_paid = models.IntegerField(default=0)
    total_discount = models.IntegerField(default=0)
    order_count = models.IntegerField(default=0)
    item_count = models.IntegerField(default=0)
    active_order = models.IntegerField(null=True, blank=True)