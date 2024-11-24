from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import (render, redirect)
from django.db import transaction

from .billingaddress import Billing
from .forms import UserAddressForm
from .models import BillingAddress


@login_required
def address_session_view(request):
	billing_session = Billing(request)
	if request.POST.get('action') == 'post':
		address = BillingAddress.objects.get(customer=request.user, default=True)
		billing_session.addBillingObject(address=address, uid=request.user.id)
	response = JsonResponse('successfully added address', safe=False)
	return response


@login_required
def address_list(request):
	addresses = BillingAddress.objects.filter(customer=request.user)

	return render(request, "address/list.html", {
		'addresses': addresses,
		'checkout': True if 'checkout' in request.META['HTTP_REFERER'] else False
	})


@login_required
def add_address(request):
	"""
    View for adding a new billing address.
    Handles both GET and POST requests with proper validation and error handling.
    """
	template_name = 'address/add.html'
    
    # Check if coming from checkout page
	checkout = request.META.get('HTTP_REFERER', '').find('checkout') != -1

	if request.method != 'POST':
		return render(request, template_name, {
			'form': UserAddressForm(),
			'checkout': checkout
		})

	form = UserAddressForm(request.POST)
	if not form.is_valid():
		return render(request, template_name, {
			'form': form,
			'checkout': checkout
		})

	try:
		with transaction.atomic():
			# Create new address instance but don't save yet
			address = form.save(commit=False)
			address.customer = request.user
			address.default = True
			
			# Bulk update all existing addresses to non-default
			BillingAddress.objects.filter(customer=request.user).update(default=False)
			
			# Save the new address
			address.save()
			
			messages.success(request, 'New Delivery Address has been added')
			return redirect('address:addresses')
			
	except Exception as e:
		messages.error(request, 'Error saving address. Please try again.')
		return render(request, template_name, {
			'form': form,
			'checkout': checkout
		})


@login_required
def edit_address(request, id):
	address = BillingAddress.objects.get(pk=id, customer=request.user)
	if request.POST:
		address_form = UserAddressForm(request.POST, instance=address)
		if address_form.is_valid():
			address_form.save()
			return redirect('address:addresses')
		else:
			return render(request, 'address/add', {
				'form': address_form
			})

	address_form = UserAddressForm(instance=address)
	return render(request, 'address/add.html', {
		'form': address_form
	})


@login_required
def delete_address(request, id):
	try:
		BillingAddress.objects.get(pk=id, customer=request.user).delete()
		messages.success(request, 'Address successfully deleted.')
	except BillingAddress.DoesNotExist:
		messages.error(request, 'Address doesn\'t exist.')
	return redirect('address:addresses')


@login_required
def default_address(request, id):
	try:
		address = BillingAddress.objects.get(pk=id, customer=request.user)
		BillingAddress.objects.filter(customer=request.user).update(default=False)
		address.default = True
		address.save()
	except BillingAddress.DoesNotExist:
		messages.error(request, 'Error: Address doesn\'t exist.')

	return redirect('address:addresses')
