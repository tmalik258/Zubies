from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View
from django.db.models import BooleanField, Case, When, Q

# from .forms import ProductForm
from .models import ProductImages, Product, Category
from account.models import User


# Create your views here.
class HomeView(ListView):
    model = Category
    queryset = Category.objects.filter(level=1, posts__is_active=True).distinct().order_by("name")
    template_name = 'store/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist_listings = []
        if self.request.user.is_authenticated:
            wishlist_listings = self.request.user.user_wishlist.all()
        context['wishlist_listings'] = wishlist_listings
        return context


def AboutUsView(request):
    return render(request, 'store/about_us.html')


class CategoryListView (ListView):
    model = Product
    paginate_by = 12
    template_name = 'store/products.html'

    def get_queryset(self, **kwargs):
        # qs = super().get_queryset(**kwargs)
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        return Product.products.filter(category__in=category.get_descendants(include_self=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist_listings = []
        if self.request.user.is_authenticated:
            wishlist_listings = self.request.user.user_wishlist.all()
        context['wishlist_listings'] = wishlist_listings
        context['heading'] = self.kwargs['category_slug']
        return context


# class FeaturedCategoryListView (ListView):
#     model = Product
#     queryset = Product.products.filter(category__in=Category.objects.filter(is_featured=True))
#     paginate_by = 12
#     template_name = 'store/products.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         wishlist_listings = []
#         if self.request.user.is_authenticated:
#             wishlist_listings = self.request.user.user_wishlist.all()
#         context['wishlist_listings'] = wishlist_listings
#         context['heading'] = 'Featured Products'
#         return context


class MaterialListView (ListView):
    model = Product
    paginate_by = 12
    template_name = 'store/products.html'

    def get_queryset(self, **kwargs):
        qs = Product.products.all()
        return qs.filter(material__material__slug=self.kwargs['material_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist_listings = []
        if self.request.user.is_authenticated:
            wishlist_listings = self.request.user.user_wishlist.all()
        context['wishlist_listings'] = wishlist_listings
        context['heading'] = self.kwargs['material_slug']
        return context


# class BrandsListView (ListView):
#     model = Product
#     paginate_by = 12
#     template_name = 'store/products.html'

#     def get_queryset(self, **kwargs):
#         qs = Product.products.all()
#         return qs.filter(brand__isnull=False)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         wishlist_listings = []
#         if self.request.user.is_authenticated:
#             wishlist_listings = self.request.user.user_wishlist.all()
#         context['wishlist_listings'] = wishlist_listings
#         context['heading'] = 'Brands'
#         return context


# class BrandProductListView (ListView):
#     model = Product
#     paginate_by = 12
#     template_name = 'store/products.html'

#     def get_queryset(self, **kwargs):
#         qs = Product.products.all()
#         return qs.filter(brand__slug=self.kwargs['brand_slug'])

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         wishlist_listings = []
#         if self.request.user.is_authenticated:
#             wishlist_listings = self.request.user.user_wishlist.all()
#         context['wishlist_listings'] = wishlist_listings
#         context['heading'] = 'Brand'
#         brand = Brand.objects.get(slug=self.kwargs['brand_slug'])
#         context['sub_heading'] = self.kwargs['brand_slug']
#         if brand.logo:
#             context['brand_logo'] = brand.logo.url
#         return context


class ItemDetailView (DetailView):
    model = Product
    template_name = 'store/product.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post = Product.products.get(slug=self.kwargs['slug'])
    #     is_added_to_wishlist = False

    #     if request.user.is_authenticated:
    #         is_added_to_wishlist = post.user_wishlist.filter(id=request.user.id).exists()
    #         if request.user.username == post.creator.username:
    #             active = True
        
    #     context['is_added_to_wishlist'] = is_added_to_wishlist
    #     return context


# @staff_member_required
# def create_product(request):
#     if request.method == "POST":
#         product_form = ProductForm(request.POST)
#         images = request.FILES.getlist('images')

#         if product_form.is_valid():
#             product_form.save()

#             for img in images:
#                 ProductImages.objects.create(item=product_form, image=img)

#             messages.success(request, "Yeew, check it out on the home page!")
#             return redirect("store:index")

#         else:
#             for field in product_form:
#                 for error in field.errors:
#                     messages.error(request, f"{field.name}: {error}")

#             print(product_form.errors)
#             return render(
#                 request, 'store/createProduct.html', {
#                     'form': product_form
#                 })

#     product_form = ProductForm()
#     return render(request, 'store/createProduct.html', {
#         'form': product_form,
#     })
