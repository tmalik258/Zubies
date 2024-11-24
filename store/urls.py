from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
	# Home Url
	path('', views.HomeView.as_view(), name='index'),

	# Catalog Url
	path('catalog/', views.CatalogView.as_view(), name='catalog'),
	path('catalog/<str:category_title>/', views.CatalogView.as_view(), name='catalog_category'),
	# Category Url
	path('category/<uuid:category_id>/', views.CategoryListView.as_view(), name='products-by-category'),
	# Features Url
	path('collection/<slug:collection_slug>/', views.CollectionListView.as_view(), name='products-by-collection'),
	# Discount Url
	path('discount/', views.DiscountListView.as_view(), name='discount-products'),

	# Product Detail Url
	path('product/<slug>/', views.ProductDetailView.as_view(), name='product'),

	# About Us Url
	path('about-us/', views.AboutView.as_view(), name='about-us'),
	# Contact Us API Url
	path('contact/', views.contact_view, name='contact-us')
]
