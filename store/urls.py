from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
	# Home Url
	path('', views.HomeView.as_view(), name='index'),
	# Category Url
	path('category/<slug:category_slug>/', views.CategoryListView.as_view(), name='products-by-category'),
	# Features Url
	path('featured-products/<slug:featured_slug>/', views.FeaturedCategoryListView.as_view(), name='product-by-featured-categories'),
	# Product Detail Url
	path('product/<slug>/', views.ProductDetailView.as_view(), name='product'),
	# About Us
	path('about-us/', views.AboutView.as_view(), name='about-us'),
]
