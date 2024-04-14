from django.shortcuts import render
from django.http import JsonResponse

from .models import NewsLetter, BecomeSeller, BecomeSellerImage
from .forms import BecomeSellerForm

# Create your views here.
def SubscribeView(request):
	if request.POST:
		email = request.POST.get('email')
		if request.POST.get('action') == 'subscribe':
			newsltr, create = NewsLetter.objects.get_or_create(email=email)
			if create:
				response = JsonResponse('🎉 Congratulations and Welcome to Our Website\'s Subscriber Family! 🎉', safe=False)
			else:
				response = JsonResponse('You Have Already Been Subscribed!', safe=False)

	return response


def BecomeSellerView(request):
	if request.method == "POST":
		seller_form = BecomeSellerForm(request.POST)
		images = request.FILES.getlist('images')

		if seller_form.is_valid():
			seller_form.save()

			for img in images:
				BecomeSellerImage.objects.create(seller=seller_form, image=img)

			messages.success(request, "Yeew, check it out on the home page!")
			return redirect("store:index")

		else:
			print(f"seller form errors: {seller_form.errors}")
			return render(
				request, 'store/createProduct.html', {
					'form': seller_form
				})

	form = BecomeSellerForm()
	return render(request, 'more/sellerform.html', {
		'form': form
	})
