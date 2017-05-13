# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from front.models import Product
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator,MaxValueValidator
from coupons.models import Coupon

class Order(models.Model):
    
    username = models.CharField(max_length=255, null=True)
    firstname = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,related_name='orders',null=True,blank=True)
    discount = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Order {}'.format(self.id)
    def get_total_cost(self):
        total_cost=sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost*(self.discount/Decimal('100'))

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)
    def get_cost(self):
        return self.price*self.quantity
    
    




