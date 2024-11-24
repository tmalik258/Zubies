import pytz
from django.contrib import admin
from django.utils.translation import gettext as _

from .models import (Order, OrderItem, OrderItemAttribute)


# Order Items Model
class OrderItemAttributeInline(admin.TabularInline):
	model = OrderItemAttribute
	fk_name = 'order_item'
	verbose_name = _("Order Item Attribute")
	verbose_name_plural = _("Order Item Attributes")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	inlines = [OrderItemAttributeInline,]
	list_filter = ('item', 'order', 'order__id')
	list_display = ('item', 'order', 'quantity', 'is_cancelled')


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	fk_name = 'order'
	verbose_name = _("Order Item")
	verbose_name_plural = _("Order Items")


# Order Model
@admin.register(Order)
class OrderAdmin (admin.ModelAdmin):
	inlines = [OrderItemInline,]
	list_display = ('user', 'total_payment', 'is_cancelled', 'paid', 'delivered', 'order_status', 'delivery_status', 'get_local_created_at', 'get_local_updated_at', 'delivered_date')
	readonly_fields = ['get_local_created_at', 'get_local_updated_at']
	list_filter = ('user', 'paid', 'items', 'delivered', 'order_created', 'order_status', 'delivery_status', 'delivered_date')
	list_editable = ['paid', 'order_status', 'delivery_status', 'delivered']
	empty_value_display = '-'

	def get_local_created_at(self, obj):
		if obj.order_created:
			pakistan_tz = pytz.timezone('Asia/Karachi')
			local_time = obj.order_created.astimezone(pakistan_tz)
			return local_time.strftime("%d-%m-%Y %H:%M:%S")
	get_local_created_at.short_description = 'Created At (Pakistan Time)'

	def get_local_updated_at(self, obj):
		if obj.order_updated:
			pakistan_tz = pytz.timezone('Asia/Karachi')
			local_time = obj.order_updated.astimezone(pakistan_tz)
			return local_time.strftime("%d-%m-%Y %H:%M:%S")
	get_local_updated_at.short_description = 'Updated At (Pakistan Time)'