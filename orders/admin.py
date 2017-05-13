# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.core.urlresolvers import reverse

def order_detail(obj):
    return '<a href="{}">View</a>'.format(reverse('orders:admin_order_detail',args=[obj.id]))
order_detail.allow_tags = True


def export_to_csv(modeladmin,request,queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields =[field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row=[]
        for field in fields:
            value = getattr(obj,field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description='Export to CSV'


def detailed_csv(modeladmin,request,queryset):
    for obj in queryset:
        id=obj.id
        order = Order.objects.get(id=id)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename={}.csv'.format(order.id)
        writer = csv.writer(response)

        order_titles = ['order ID' , 'username','firstname','email','phone_number','location','coupon','discount']
        fields = [order.id, order.username, order.firstname, order.email, order.phone_number,order.location,order.coupon,order.discount]
        product_titles = ['Product','Price','Quantity','Cost(UGX)']
        summary_titles = ['company', 'total sum']
        summary_values = ['identity UG  2017', order.get_total_cost()]
        paid = ['CASH ON DELIVERY']



        writer.writerow(['***ORDER DETAILS***'])
        writer.writerow([])
        writer.writerow(order_titles)
        writer.writerow(fields)
        writer.writerow([])
        writer.writerow(['***PURCHASE DETAILS***'])
        writer.writerow([])
        writer.writerow(product_titles)


        for item in order.items.all():

            product_values=[]
            product_values.append(item.product.name)
            product_values.append(item.price)
            product_values.append(item.quantity)
            product_values.append(item.get_cost())
            writer.writerow(product_values)

        writer.writerow([])
        writer.writerow(['***TOTAL SUM DETAILS***'])
        writer.writerow(summary_titles)
        writer.writerow(summary_values)
        writer.writerow([])
        writer.writerow(['***PAYMENT STATUS***'])

        writer.writerow(paid)
    return response

detailed_csv.short_description='Export to detailed CSV'
   
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','username','firstname','email','phone_number','location','created','updated','paid','coupon',
                  'discount',order_detail]
    #list_filter = ['paid','created','updated']
    inlines=[OrderItemInline]
    actions = [detailed_csv,export_to_csv]
    

admin.site.register(Order,OrderAdmin)



