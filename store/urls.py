from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
	# Home Url
	path('', views.HomeView.as_view(), name='index'),
	# Category Url
	path('category/<slug:category_slug>/', views.CategoryListView.as_view(), name='products-by-category'),
	# Features Url
	# path('?featured-products', views.FeaturedCategoryListView.as_view(), name='product-by-featured-categories'),
	# Material Url
	path('material/<slug:material_slug>/', views.MaterialListView.as_view(), name='products-by-material'),
	# # Brand Url
	# path('brands/', views.BrandsListView.as_view(), name='products-by-brands'),
	# # Brand Individual Url
	# path('brand/<slug:brand_slug>/', views.BrandProductListView.as_view(), name='products-by-brand'),
	# Create Product Url
	path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
	# About Us
	path('about-us/', views.AboutUsView, name='about-us'),
]
