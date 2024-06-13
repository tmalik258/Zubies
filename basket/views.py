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
		if request.POST.get('action') == 'add':
			product_id = int(request.POST.get('productId'))
			product = get_object_or_404(Product, id=product_id)
			product_qty = int(request.POST.get('product_qty'))
			attribute_id = request.POST.get('attribute_id')
			basket.add(product=product, qty=product_qty, attributes=attribute_id)

		elif request.POST.get('action') == 'update':
			item_key = str(request.POST.get('key'))
			product_qty = int(request.POST.get('product_qty'))
			basket.update(item_key=item_key, qty=product_qty)

		elif request.POST.get('action') == 'delete':
			item_key = str(request.POST.get('key'))
			basket.delete(item_key=item_key)

		basketqty = basket.__len__()
		basketTotal = basket.get_total_price()
		response = JsonResponse({'qty': basketqty, 'subtotal': basketTotal})
		return response