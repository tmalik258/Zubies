from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.utils.translation import gettext as _
from django.contrib import messages

from .models import (
	Category,
	FeaturedCategory,
	Material,
	Product,
	ProductSpecification,
	ProductSpecificationValue,
	ProductImages,
)

# Register your models here.
admin.site.register(ProductSpecification)


# Category Model
@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
	list_display = ["name", "slug"]
	prepopulated_fields = {"slug": ("name",)}

# Featured Category Model
@admin.register(FeaturedCategory)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ["name", "slug"]
	prepopulated_fields = {"slug": ("name",)}

# Material Model
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
	list_display = ["name"]


# ProductSpecificationValue Inline Model
class ProductSpecificationValueInline(admin.TabularInline):
	model = ProductSpecificationValue


# Image Inline Model
class ImageInline(admin.TabularInline):
	model = ProductImages
	fk_name = "item"
	max_num = 5
	verbose_name_plural = _("image")


# Product Model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	inlines = [
		ProductSpecificationValueInline,
		ImageInline,
	]
	list_display = (
		"title",
		"regular_price",
		"discount_price",
		'sku',
		'stock',
		"in_stock",
		"is_active",
		"category",
		"created",
		"updated",
		"image_tag",
	)
	list_filter = (
		"regular_price",
		"discount_price",
		"in_stock",
		"is_active",
		"category",
		"created",
	)
	list_editable = ["regular_price", "discount_price", "stock", "is_active"]
	prepopulated_fields = {"slug": ("title",)}
	empty_value_display = "-empty-"


	@admin.action
	def make_active (self, request, queryset):
		queryset.update(active=True)
		messages.success(request, "Selected Record(s) Marked as Active Successfully !!")

	@admin.action
	def make_inactive (self, request, queryset):
		queryset.update(active=False)
		messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")

	actions = ['make_active', 'make_inactive']


# Image Model
class ImageAdmin(admin.ModelAdmin):
	list_display = ("item", "image_tag")
	list_filter = ("item",)


admin.site.register(ProductImages, ImageAdmin)
