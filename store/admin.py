from django.core.files.uploadedfile import UploadedFile
import os
from django import forms
from django.contrib import (admin, messages)
from django.utils.translation import gettext as _

from mptt.admin import MPTTModelAdmin

from .models import (
	Category,
	FeaturedCategory,
	Material,
	Product,
	ProductSpecification,
	ProductSpecificationValue,
	ProductImage,
)


admin.site.register(ProductSpecification)


# Category Model
@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
	list_display = ["name", "slug"]


# Featured Category Model
@admin.register(FeaturedCategory)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ["name", "slug"]


# Material Model
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
	list_display = ["name"]


# ProductSpecificationValue Inline Model
class ProductSpecificationValueInline(admin.TabularInline):
	model = ProductSpecificationValue


# Image Inline Model
class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 0
	can_delete = True
	verbose_name_plural = 'Images'
	fields = ('image', 'alt_text')


class MultipleFileInput(forms.ClearableFileInput):
	allow_multiple_selected = True


class MultipleFileField(forms.FileField):
	def __init__(self, *args, **kwargs):
		kwargs.setdefault("widget", MultipleFileInput())
		super().__init__(*args, **kwargs)
	
	def clean(self, data, initial=None):
		single_file_clean = super().clean
		if isinstance(data, (list, tuple)):
			result = [single_file_clean(d, initial) for d in data]
		else:
			result = single_file_clean(data, initial)
		return result


class ProductAdminForm(forms.ModelForm):
	images = MultipleFileField(required=False)

	class Meta:
		model = Product
		fields = '__all__'


# Product Model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	form = ProductAdminForm
	inlines = [
		ProductSpecificationValueInline,
		ProductImageInline,
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
	empty_value_display = "-empty-"

	def save_model(self, request, obj, form, change) -> None:
		super().save_model(request, obj, form, change)
		images = request.FILES.getlist('images')

		for image in images:
			if isinstance(image, UploadedFile):
            # Get the filename without extension
				filename = os.path.splitext(image.name)[0]
				
				# Create ProductImage with alt_text
				ProductImage.objects.create(
					product=obj,
					image=image,
					alt_text=filename
				)
			else:
				print(f"Unexpected type for image: {type(image)}")


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
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
	list_display = ("product", "image_tag")
	list_filter = ("product",)
