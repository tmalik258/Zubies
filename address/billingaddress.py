from django.conf import settings


class Billing():
	"""
	A base billing class, providing some default behaviors that can be inherited or overrided, as necessary.
	"""

	def __init__(self, request):
		self.session = request.session
		billing_address = self.session.get(settings.BILLING_ADDRESS_SESSION_ID)

		if settings.BILLING_ADDRESS_SESSION_ID not in request.session:
			billing_address = self.session[settings.BILLING_ADDRESS_SESSION_ID] = {}
		self.billing_address = billing_address
		# print(self.billing_address)

	def add(self, bform, uid):
		"""
		Adding and updating the users billing session data via billing form
		"""
		self.billing_address[uid] = {
			'first_name': bform.cleaned_data['first_name'],
			'last_name': bform.cleaned_data['last_name'],
			'email': bform.cleaned_data['email'],
			'phone_number': bform.cleaned_data['phone_number'],
			'address_line_1': bform.cleaned_data['address_line_1'],
			'address_line_2': bform.cleaned_data['address_line_2'],
			'city': bform.cleaned_data['city'],
			'state': bform.cleaned_data['state'],
			'country': bform.cleaned_data['country'],
			'zip_code': bform.cleaned_data['zip_code'],
			'payment_method': bform.cleaned_data['payment_method'],
		}

		self.save()

	def addBillingObject(self, address, uid):
		"""
		Adding and updating the users billing session data via Billing object
		"""
		self.billing_address[uid] = {
			'first_name': str(address.first_name),
			'last_name': str(address.last_name),
			'email': str(address.email),
			'phone_number': str(address.phone_number),
			'address_line_1': str(address.address_line_1),
			'address_line_2': str(address.address_line_2),
			'city': str(address.city),
			'state': str(address.state),
			'country': str(address.country),
			'zip_code': str(address.zip_code),
			'payment_method': 'COD'
		}
		print(self.billing_address)
		self.save()

	def exists(self):
		"""
		Returns true if session contains billing address else false
		"""
		if self.billing_address != {}:
			return True
		else:
			return False

	def save(self):
		self.session.modified = True

	def clear(self):
		del self.session[settings.BILLING_ADDRESS_SESSION_ID]
		self.save()