import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

# Create your models here.

class BillingAddress (models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	# Customer
	customer = models.ForeignKey("account.User", on_delete=models.CASCADE, verbose_name=_("Customer"), blank=True, null=True)
	first_name = models.CharField(_("First Name"), max_length=150)
	last_name = models.CharField(_("Last Name"), max_length=150)
	email = models.EmailField()
	# Delivery Details
	phone_number = models.CharField(_("Phone Number"), max_length=15)
	address_line_1 = models.CharField(_("Address Line 1"), max_length=150)
	address_line_2 = models.CharField(_("Address Line 2"), max_length=150, blank=True)
	city = models.CharField(_("City"), max_length=150)
	state = models.CharField(_("State/Province/Region"), max_length=150)
	country = CountryField(_("Country"), blank_label='Country')
	zip_code = models.CharField(_("Zip Code"), max_length=12)
	default = models.BooleanField(_("Default"), default=False)

	class Meta:
		verbose_name = 'Billing Address'
		verbose_name_plural = 'Billing Addresses'

	def __str__(self):
		return self.customer.username