import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .basket import Basket
from store.models import Product


def basket_summary(request):
	return render(request, 'basket/cart.html')


def basket_update(request):
    basket = Basket(request)

    if request.POST:
        if request.POST.get('action') == 'add':
            try:
                product_id = int(request.POST.get('productId'))
                product = get_object_or_404(Product, id=product_id)
                product_qty = int(request.POST.get('product_qty'))
                
                attribute_ids = json.loads(request.POST.get('attribute_ids'))
                print(attribute_ids)
                # # Convert string IDs to integers if needed
                # attribute_ids = [int(id_) for id_ in attribute_ids]
                
                basket.add(product=product, qty=product_qty, attributes=attribute_ids)

            except (ValueError, json.JSONDecodeError) as e:
                return JsonResponse({
                    'error': 'Invalid data provided',
                    'details': str(e)
                }, status=400)

        elif request.POST.get('action') == 'update':
            try:
                item_key = str(request.POST.get('key'))
                product_qty = int(request.POST.get('product_qty'))
                basket.update(item_key=item_key, qty=product_qty)

            except ValueError as e:
                return JsonResponse({
                    'error': 'Invalid data provided',
                    'details': str(e)
                }, status=400)

        elif request.POST.get('action') == 'delete':
            try:
                item_key = str(request.POST.get('key'))
                basket.delete(item_key=item_key)

            except ValueError as e:
                return JsonResponse({
                    'error': 'Invalid data provided',
                    'details': str(e)
                }, status=400)

        basketqty = basket.__len__()
        basketSubTotal = basket.get_after_discount_subtotal_price()
        return JsonResponse({
            'qty': basketqty, 
            'subtotal': basketSubTotal
        })

    return JsonResponse({
        'error': 'Invalid request method'
    }, status=405)