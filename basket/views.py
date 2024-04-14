from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .basket import Basket
from store.models import Product

# Create your views here.
def basket_summary(request):
	basket = Basket(request)
	return render(request, 'basket/summary.html', {
		'basket': basket
	})

def basket_update(request):
	basket = Basket(request)

	if request.POST:
		product_id = int(request.POST.get('productId'))
		product = get_object_or_404(Product, id=product_id)
		if request.POST.get('action') == 'add':
			product_qty = int(request.POST.get('product_qty'))
			basket.add(product=product, qty=product_qty)

		elif request.POST.get('action') == 'update':
			product_qty = int(request.POST.get('product_qty'))
			basket.update(product=product, qty=product_qty)

		elif request.POST.get('action') == 'delete':
			basket.delete(product=product)

		basketqty = basket.__len__()
		basketTotal = basket.get_total_price()
		response = JsonResponse({'qty': basketqty, 'subtotal': basketTotal})
		return response
