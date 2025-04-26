import uuid
from decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.forms import ValidationError
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils.safestring import mark_safe

from mptt.models import MPTTModel, TreeForeignKey

from abstract.models import AbstractMediaModel


# Model Managers
class ProductManager(models.Manager):
	def get_queryset(self):
		return super(ProductManager, self).get_queryset().filter(is_active=True, in_stock=True)


# Models
class Category (MPTTModel):
	"""
	Category table implimented with MPTT
	"""
	category_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	title = models.CharField(
		verbose_name=_("Category Name"),
		help_text=_("Required and unique"),
		max_length=124,
	)
	is_active = models.BooleanField(default=True)
	parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

	class MPTTMeta:
		order_insertion_by = ["title"]

	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")
		indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['category_id']),
        ]

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('store:products-by-category', kwargs={
			'category_id': self.category_id
		})

	def get_images(self):
		"""
		Get all related images for the category with caching
		"""
		cache_key = f'category_images_{self.id}'
		images = cache.get(cache_key)
		
		if images is None:
			# Get content type once and cache it
			content_type_cache_key = 'category_content_type'
			content_type = cache.get(content_type_cache_key)
			
			if content_type is None:
				content_type = ContentType.objects.get_for_model(self.__class__)
				cache.set(content_type_cache_key, content_type, timeout=3600 * 24)  # Cache for 24 hours
			
			# Fetch images with select_related for any foreign keys if needed
			images = list(CategoryMedia.objects.select_related(
				'content_type'
			).filter(
				content_type=content_type,
				object_id=self.id
			).order_by('id'))  # Add appropriate ordering
			
			# Cache the images for 1 hour
			cache.set(cache_key, images, timeout=3600)
		
		return images


class CategoryMedia(AbstractMediaModel):
	"""
	Category Images
	"""

	class Meta:
		verbose_name = _("Category Image")
		verbose_name_plural = _("Category Images")



class Collection (models.Model):
	"""
	Collections like seasoned, new articles, best-selling
	"""
	name = models.CharField(verbose_name=_("Collection Name"), help_text=_("Required"), max_length=255)
	slug = models.SlugField(verbose_name=_("Collection Safe URL"), max_length=255, unique=True, editable=False)

	class Meta:
		verbose_name = _("Collection")
		verbose_name_plural = _("Collections")

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('store:product-by-collection', kwargs={
			'collection_slug': self.slug
		})

	def save (self, *args, **kwargs):
		value = self.name.replace(" ", "-")
		self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)


class Material (models.Model):
	"""
	Product made by which material
	"""

	name = models.CharField(verbose_name=_("Material Name"), help_text=_("Required"), max_length=255)

	def __str__(self):
		return self.name


class ProductSpecification(models.Model):
	"""
	The Product Specification Table contains product specification of features for the product types
	"""

	name = models.CharField(verbose_name=_("Attribute Name"), help_text=_("Required"), max_length=255)
	

	class Meta:
		verbose_name = _("Product Specification")
		verbose_name_plural = _("Product Specifications")

	def __str__(self):
		return self.name


class ProductSpecificationValue(models.Model):
	"""
	The Product Specification Value table holds each of the products individual specification or bespoke features
	"""
	
	product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="specification")
	specification = models.ForeignKey("ProductSpecification", on_delete=models.CASCADE)
	value = models.CharField(verbose_name=_("Attribute Value"), max_length=255, help_text=_("Product Specification Value (maximum of 255 characters)"))


	class Meta:
		verbose_name = _("Product Specification Value")
		verbose_name_plural = _("product Specification Values")

	def __str__(self):
		return self.value


class Product (models.Model):
	"""
	The Product table containing all product items
	"""
	title = models.CharField(max_length=255, unique=True, help_text=_("Required"))
	slug = models.SlugField(max_length=255, unique=True, editable=False)
	regular_price = models.DecimalField(verbose_name=_("Regular Price"), max_digits=10, decimal_places=2, help_text=_("Maximum 99999999.99"), error_messages={
		"name": {
			"max_length": _("The price must be between 0 and 99999999.99."),
		},
	})
	discount_price = models.DecimalField(verbose_name=_("Discount Price"), max_digits=10, decimal_places=2, help_text=_("Maximum 99999999.99"), error_messages={
		"name": {
			"max_length": _("The price must be between 0 and 99999999.99."),
		},
	}, blank=True, null=True)
	manufacturing_cost = models.DecimalField(verbose_name=_("Manufacturing Cost"), max_digits=10, decimal_places=2, help_text=_("Maximum 99999999.99"), error_messages={
		"name": {
			"max_length": _("The price must be between 0 and 99999999.99."),
		},
	}, blank=True, null=True)
	description = models.TextField(help_text=_("Required"))
	sku = models.CharField(default='123', max_length=124)
	category = TreeForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
	collection = models.ManyToManyField(Collection, related_name="posts")
	material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="posts", blank=True, null=True)
	weight = models.DecimalField(default=Decimal("0"), max_digits=10, decimal_places=3, help_text=_('kg'))
	stock = models.IntegerField(default=0)
	in_stock = models.BooleanField(default=True)
	is_active = models.BooleanField(verbose_name=_("Product Visibility"), help_text=_("Change Product Visibility"), default=True)
	wishlist = models.ManyToManyField(get_user_model(), related_name='wishlist', blank=True)
	created = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True, editable=False)
	updated = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

	objects = models.Manager()
	products = ProductManager()

	class Meta:
		verbose_name = _("Product")
		verbose_name_plural = _("Products")
		ordering = ('-created',)
		indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['slug']),
        ]

	def save (self, *args, **kwargs):
		value = self.title.replace(" ", "-")
		self.slug = slugify(value, allow_unicode=True)

		self.in_stock = self.stock > 0

		super().save(*args, **kwargs)

	def clean(self):
		if self.weight < Decimal("0"):
			raise ValidationError("Weight cannot be negative.")

	def get_absolute_url(self):
		return reverse('store:product', kwargs={
			'slug': self.slug
		})

	def image_tag(self):
		"""Get first image only"""
		f_image = ProductMedia.objects.filter(content_type__model='product', object_id=self.id).first()
		if f_image:
			return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % f_image.image.url)
		else:
			return 'No image found'
	image_tag.short_description = 'Image'

	def get_images(self):
		"""
		Get all related images with caching
		"""
		cache_key = f'product_images_{self.id}'
		images = cache.get(cache_key)

		if images is None:
			content_type_cache_key = 'product_content_type'
			content_type = cache.get(content_type_cache_key)

			if content_type is None:
				content_type = ContentType.objects.get_for_model(self.__class__)
				cache.set(content_type_cache_key, content_type, timeout=3600 * 24)  # Cache for 24 hours

			images = list(ProductMedia.objects.select_related(
				'content_type'
			).filter(
				content_type=content_type,
				object_id=self.id
			).order_by('id'))

			# Cache for 1 hour
			cache.set(cache_key, images, timeout=3600)

		return images

	def is_in_wishlist(self, user):
		"""Check if product is in user's wishlist"""
		if not user.is_authenticated:
			return False
		return self.wishlist.filter(id=user.id).exists()

	def __str__(self):
		return self.title


class ProductMedia (AbstractMediaModel):
	"""
    Product Images
    """

	class Meta:
		verbose_name = _("Product Image")
		verbose_name_plural = _("Product Images")