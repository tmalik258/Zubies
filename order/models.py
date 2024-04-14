from django.conf import settings
from django_countries.fields import CountryField
from django.db import models

from store.models import Product

# Create your models here.


class Order (models.Model):
	ORDER_STATUS_CHOICES = (
		('F', 'Fullfilled'),
		('P', 'In Process'),
	)
	DELIVERY_STATUS_CHOICES = (
		('D', 'Delivered'),
		('P', 'In Process'),
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order', blank=True, null=True)
	items = models.ManyToManyField('OrderItem')

	# payment
	total_payment = models.DecimalField(max_digits=10, decimal_places=2)
	paid = models.BooleanField(default=False)
	PAYMENT_CHOICES = (
		('COD', 'Cash on Delivery'),
	)
	payment = models.CharField(max_length=15, choices=PAYMENT_CHOICES, default='COD')

	# order
	order_created = models.DateTimeField(auto_now_add=True)
	order_updated = models.DateTimeField(auto_now=True)
	order_status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default='P')

	# cancel
	is_cancel_allowed = models.BooleanField(default=True)
	is_cancelled = models.BooleanField(default=False)

	# delivery
	delivery_status = models.CharField(max_length=2, choices=DELIVERY_STATUS_CHOICES, default='P')
	delivered_date = models.DateTimeField(blank=True, null=True)
	delivered = models.BooleanField(default=False)

	# billing address details
	# required
	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=25)
	email = models.EmailField()
	# optional, that if billing address exits then no need to reenter data into these fields
	phone_number = models.CharField(max_length=15, blank=True, null=True)
	address_line_1 = models.CharField(max_length=150, blank=True, null=True)
	address_line_2 = models.CharField(max_length=150, blank=True, null=True)
	city = models.CharField(max_length=150, blank=True, null=True)
	state = models.CharField(max_length=150, blank=True, null=True)
	country = CountryField(blank_label='Country', blank=True, null=True)
	zip_code = models.CharField(max_length=12, blank=True, null=True)
	billing_address = models.ForeignKey("address.BillingAddress", on_delete=models.SET_NULL, blank=True, null=True)

	class Meta:
		ordering = ('-order_created',)

	def __str__(self):
		order_placed = self.order_created.strftime("%I:%M %p | %d-%m-%Y")
		return f"{self.user.first_name} {self.user.last_name} | {order_placed}"

	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total


class OrderItem (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_items', blank=True, null=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()


class OrderItemAttribute(models.Model):
    order_item = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, related_name="order_item_attribute"
    )
    attribute = models.ForeignKey('store.ProductSpecificationValue', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attribute.specification.name}: {self.attribute.value}"
