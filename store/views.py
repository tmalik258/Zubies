import logging
import json

from django.http import JsonResponse, Http404
from django.db.models import Exists, OuterRef
from django.core.mail import send_mail
from django.views.generic import DetailView, ListView, TemplateView
from django.views.decorators.csrf import csrf_protect

from store.decorators import rate_limit
from store.forms import ContactForm

from .models import Product, Category, Collection


logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'store/index.html'


class AboutView(TemplateView):
    template_name = 'store/about_us.html'


class CatalogView(ListView):
	model = Product
	paginate_by = 12
	template_name = 'store/list.html'

	def get_queryset(self, **kwargs):
		category_title = self.kwargs.get('category_title')

		if not category_title:
			if self.request.user.is_authenticated:
				return Product.products.all().annotate(
					is_wishlisted=Exists(
						Product.objects.filter(
							id=OuterRef('id'),
							wishlist=self.request.user
						)
					)
				)
			return Product.products.all()

		try:
			category = Category.objects.get(title__iexact=category_title.replace("-", " ").title())
			if self.request.user.is_authenticated:
				return Product.products.filter(category__in=category.get_descendants(include_self=True)).annotate(
					is_wishlisted=Exists(
						Product.objects.filter(
							id=OuterRef('id'),
							wishlist=self.request.user
						)
					)
				)
			return Product.products.filter(category__in=category.get_descendants(include_self=True))
		except Category.DoesNotExist:
			raise Http404('Category doesn\'t exists.')


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['heading'] = self.kwargs['category_title'].replace("-", " ").title() if self.kwargs.get('category_title') else 'Catalog'
		return context


class CategoryListView (ListView):
	model = Product
	paginate_by = 12
	template_name = 'store/list.html'

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		try:
			self.category: Category = Category.objects.get(category_id=self.kwargs['category_id'])
		except Category.DoesNotExist:
			raise Http404("Category does not exist")

	def get_queryset(self, **kwargs):
		if self.request.user.is_authenticated:
			return Product.products.filter(category__in=self.category.get_descendants(include_self=True)).annotate(
					is_wishlisted=Exists(
						Product.objects.filter(
							id=OuterRef('id'),
							wishlist=self.request.user
						)
					)
				)
		return Product.products.filter(category__in=self.category.get_descendants(include_self=True))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['heading'] = self.category.title if self.category else False
		return context


class CollectionListView (ListView):
	model = Product
	paginate_by = 12
	template_name = 'store/list.html'

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		try:
			self.collection: Collection = Collection.objects.get(slug=self.kwargs['collection_slug'])
		except Collection.DoesNotExist:
			raise Http404("Category does not exist")

	def get_queryset(self, **kwargs):
		if self.request.user.is_authenticated:
			return Product.products.filter(collection=self.collection).annotate(
					is_wishlisted=Exists(
						Product.objects.filter(
							id=OuterRef('id'),
							wishlist=self.request.user
						)
					)
				)
		return Product.products.filter(collection=self.collection)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['heading'] = self.collection.name if self.collection else False
		return context


class DiscountListView (ListView):
	model = Product
	paginate_by = 12
	template_name = 'store/list.html'

	def get_queryset(self):
		queryset = Product.products.filter(discount_price__isnull=False).exclude(discount_price=0)
		
		if self.request.user.is_authenticated:
			queryset = queryset.annotate(
				is_wishlisted=Exists(
					Product.objects.filter(
						id=OuterRef('id'),
						wishlist=self.request.user
					)
				)
			)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['heading'] = False
		context['discount'] = True
		return context


class ProductDetailView (DetailView):
	model = Product
	template_name = 'store/product.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		
		if self.request.user.is_authenticated:
			queryset = queryset.annotate(
				is_wishlisted=Exists(
					Product.objects.filter(
						id=OuterRef('id'),
						wishlist=self.request.user
					)
				)
			)
		return queryset


@rate_limit(limit=5, period=60)
@csrf_protect
def contact_view(request):
	if request.method != "POST":
		return JsonResponse({"error": "POST request required."}, status=405)

	# Check sender data
	try:
		data = json.loads(request.body)
	except json.JSONDecodeError as e:
		logger.error(f"Error in contact form submission: {str(e)}")
		return JsonResponse({"error": "Invalid JSON in request.body."}, status=400)

	form = ContactForm(data)

	# Validate contact form
	if form.is_valid():
		# process form data
		cleaned_data = form.cleaned_data
        # Send email
		message = f"""
        New contact form submission:
        Name: {cleaned_data['fname']} {cleaned_data['lname']}
        Email: {cleaned_data['email']}
        Message: {cleaned_data['message']}
        """
		send_mail('New Contact Form Submission', message, cleaned_data['email'], ['info@zubies.co'], fail_silently=False)
		return JsonResponse({"message": "Thankyou for contacting us."}, status=201)
	else:
		return JsonResponse({"error": form.errors}, status=400)

	# Create contact
	# contact = Contact(
	# 	fname=fname,
	# 	lname=lname,
	# 	phone_number=phone_number,
	# 	email=email,
	# 	message=message,
	# )
	# contact.save()
