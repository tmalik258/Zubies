# from django.contrib import admin
# from django.utils.translation import gettext as _

# from .models import (Order, OrderItem)

# # Register your models here.

# # Order Items Model
# admin.site.register(OrderItem)

# # Order Model
# @admin.register(Order)
# class OrderAdmin (admin.ModelAdmin):
# 	# inlines = [OrderItemInline]
# 	list_display = ('user', 'total_payment', 'paid', 'delivered', 'order_created', 'order_updated', 'order_status', 'delivery_status', 'delivered_date', 'billing_address')
# 	list_filter = ('user', 'paid', 'delivered', 'order_created', 'order_status', 'delivery_status', 'delivered_date')
# 	list_editable = ['paid', 'order_status', 'delivery_status', 'delivered']
# 	empty_value_display = '-empty-'