from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.utils.translation import gettext as _

from .models import (
	Category,
	Brand,
	Material,
	ProductMaterial,
	Product,
	ProductSpecification,
	ProductSpecificationValue,
	ProductImages,
	GridCategory,
)

# Register your models here.
admin.site.register(ProductSpecification)


# Brand Admin Model
@admin.register(GridCategory)
class GridCategoryAdmin(admin.ModelAdmin):
	list_display = ["category_name", "slug", "is_active"]
	prepopulated_fields = {"slug": ("category_name",)}
	list_editable = [
		"is_active",
	]


# Brand Admin Model
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
	list_display = ["name", "slug"]
	prepopulated_fields = {"slug": ("name",)}


# Category Model
class CategoryAdmin(MPTTModelAdmin):
	list_display = ["name", "slug"]
	prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)


# Material Model
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
	list_display = ["name", "slug"]
	prepopulated_fields = {"slug": ("name",)}


# Material Inline Model
class MaterialInline(admin.TabularInline):
	model = ProductMaterial
	fk_name = "item"
	verbose_name = _("material")
	verbose_name_plural = _("materials")


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
		MaterialInline,
		ProductSpecificationValueInline,
		ImageInline,
	]
	list_display = (
		"title",
		"regular_price",
		"slug",
		"discount_price",
		"in_stock",
		"is_active",
		"category",
		"time_created",
		"updated",
		"image_tag",
	)
	list_filter = (
		"regular_price",
		"discount_price",
		"in_stock",
		"is_active",
		"category",
		"time_created",
	)
	list_editable = ["regular_price", "discount_price", "is_active", "in_stock"]
	prepopulated_fields = {"slug": ("title",)}
	empty_value_display = "-empty-"


# 	# @admin.action
# 	# def make_active (self, request, queryset):
# 	# 	queryset.update(active=True)
# 	# 	messages.success(request, "Selected Record(s) Marked as Active Successfully !!")

# 	# @admin.action
# 	# def make_inactive (self, request, queryset):
# 	# 	queryset.update(active=False)
# 	# 	messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")

# 	# actions = ['make_active', 'make_inactive']


# Image Model
class ImageAdmin(admin.ModelAdmin):
	list_display = ("item", "image_tag")
	list_filter = ("item",)


admin.site.register(ProductImages, ImageAdmin)
