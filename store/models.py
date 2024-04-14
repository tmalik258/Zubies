from django.conf import settings
from django.db import models
from django.core.files.storage import default_storage
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
# Image Resize and Upload
from PIL import Image as PillowImage
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.safestring import mark_safe
from django.utils.crypto import get_random_string
from django.utils import timezone


# Model Managers
class ProductManager(models.Manager):
	def get_queryset(self):
		return super(ProductManager, self).get_queryset().filter(is_active=True, in_stock=True)


# Create your models here.
class GridCategory(models.Model):
	"""
	Category and related image for display on index page as grid slider
	"""
	def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/listing_<title>/<filename>
		return 'category_media/category_{0}_{1}'.format(instance.category_name, filename)

	category_name = models.CharField(verbose_name=_("Category Name"), max_length=255, unique=True)
	image = models.ImageField(verbose_name=_("Grid Category Image"), upload_to=user_directory_path)
	alt_text = models.CharField(max_length=255, verbose_name=_("Alternative Text for Image"), help_text=_("In case image is not displayed due to slow internet connection, what should be displayed instead of this image as text. Text should describe what kind of image has to be displayed"))
	slug = models.SlugField(verbose_name=_("Grid Category Safe URL"), max_length=255, unique=True)
	is_active = models.BooleanField(verbose_name=_("Visibility"), default=True)

	class Meta:
		verbose_name = _("Grid Category")
		verbose_name_plural = _("Grid Categories")

	def __str__(self):
		return self.category_name

	def get_absolute_url(self):
		if 'brands' in self.slug:
			return reverse('store:products-by-brands')
		return reverse('store:products-by-category', kwargs={
			'category_slug': self.slug
		})
		
	
	def save (self, *args, **kwargs):
		if self.image:
			img = PillowImage.open(self.image)
			# Resize image
			output_size = (1000, 1000)
			img.thumbnail(output_size)

			# Save the resized image to a BytesIO buffer
			output_buffer = BytesIO()
			img.save(output_buffer, format='WebP')
			output_buffer.seek(0)

			# Generate a unique name for the image
			random_string = get_random_string(length=8)
			timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
			filename = f'{random_string}_{timestamp}.webp'

			# Save the buffer content to the image field with the unique filename
			self.image.save(filename, ContentFile(output_buffer.read()), save=False)

		if self.slug == '':
			value = self.category_name.replace(" ", "-")
			self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)


class Category (MPTTModel):
	"""
	Category table implimented with MPTT
	"""
	name = models.CharField(
		verbose_name=_("Category Name"),
		help_text=_("Required and unique"),
		max_length=124,
		unique=True
	)
	is_featured = models.BooleanField(default=False)
	slug = models.SlugField(verbose_name=_("Category Safe URL"), max_length=255, unique=True)
	parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

	class MPTTMeta:
		order_insertion_by = ["name"]

	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('store:products-by-category', kwargs={
			'category_slug': self.slug
		})
	
	def save (self, *args, **kwargs):
		if self.slug == '':
			value = self.name.replace(" ", "-")
			self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)


class Material (models.Model):
	name = models.CharField(verbose_name=_("Material Name"), unique=True, max_length=124, db_index=True)
	slug = models.SlugField(verbose_name=_("Material Safe URL"), max_length=255, unique=True)

	class Meta:
		verbose_name = _("Material")
		verbose_name_plural = _("Materials")

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('store:products-by-material', kwargs={
			'material_slug': self.slug
		})
	
	def save (self, *args, **kwargs):
		if self.slug == '':
			value = self.name.replace(" ", "-")
			self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)


class Brand (models.Model):
	def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/listing_<title>/<filename>
		return 'logos/brands/brand_{0}/logo_{1}'.format(instance.name, filename)

	name = models.CharField(verbose_name=_("Brand Name"), unique=True, max_length=124, db_index=True)
	logo = models.ImageField(verbose_name=_("Brand Logo"), upload_to=user_directory_path, blank=True, null=True)
	slug = models.SlugField(verbose_name=_("Brand Safe URL"), max_length=255, unique=True)

	class Meta:
		verbose_name = _("Brand")
		verbose_name_plural = _("Brands")

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('store:products-by-brand', kwargs={
			'brand_slug': self.slug
		})
	
	def save (self, *args, **kwargs):
		if self.logo:
			img = PillowImage.open(self.logo)
			# Resize image
			output_size = (1000, 1000)
			img.thumbnail(output_size)

			# Save the resized image to a BytesIO buffer
			output_buffer = BytesIO()
			img.save(output_buffer, format='WebP')
			output_buffer.seek(0)

			# Generate a unique name for the image
			random_string = get_random_string(length=8)
			timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
			filename = f'{random_string}_{timestamp}.webp'

			# Save the buffer content to the image field with the unique filename
			self.logo.save(filename, ContentFile(output_buffer.read()), save=False)

		if self.slug == '':
			value = self.name.replace(" ", "-")
			self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)


class ProductMaterial(models.Model):
	material = models.ForeignKey("Material", verbose_name=_("Material Name"), on_delete=models.CASCADE)
	item = models.ForeignKey("Product", verbose_name=_("Product Name"), on_delete=models.CASCADE, related_name="material")


class ProductSpecification(models.Model):
	"""
	The Product Specification Table contains product specification of features for the product types
	"""

	name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)
	

	class Meta:
		verbose_name = _("Product Specification")
		verbose_name_plural = _("Product Specifications")

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("productspecification_detail", kwargs={"slug": self.slug})


class ProductSpecificationValue(models.Model):
	"""
	The Product Specification Value table holds each of the products individual specification or bespoke features
	"""
	
	product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="specification")
	specification = models.ForeignKey("ProductSpecification", on_delete=models.CASCADE)
	value = models.CharField(verbose_name=_("value"), max_length=255, help_text=_("Product Specification Value (maximum of 255 characters)"))


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
	description = models.TextField(help_text=_("Required"))
	# product_type = models.ForeignKey("ProductType", verbose_name=_("Type of Product"), on_delete=models.CASCADE)
	brand = models.ForeignKey("Brand", verbose_name=_("Brand"), on_delete=models.CASCADE, blank=True, null=True)
	category = TreeForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
	is_active = models.BooleanField(verbose_name=_("Product Visibility"), help_text=_("Change Product Visibility"), default=True)
	in_stock = models.BooleanField(default=True)
	weight = models.IntegerField(default=0)
	time_created = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True, editable=False)
	updated = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)
	slug = models.SlugField(max_length=255, unique=True)
	user_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_wishlist', blank=True)
	objects = models.Manager()
	products = ProductManager()

	class Meta:
		verbose_name = _("Product")
		verbose_name_plural = _("Products")
		ordering = ('-time_created',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('store:product', kwargs={
			'slug': self.slug
		})
	
	def image_tag(self):
		f_image = self.img.first()
		if f_image:
			return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % f_image.image.url)
		else:
			return 'No image found'
	image_tag.short_description = 'Image'

	def save (self, *args, **kwargs):
		if self.slug == '':
			value = self.title.replace(" ", "-")
			self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)


class ProductImages (models.Model):
	def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/listing_<title>/<filename>
		return 'product_media/item_{0}/{1}'.format(instance.item.title, filename)

	item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='img')
	image = models.ImageField(verbose_name=_("image"), upload_to=user_directory_path)
	alt_text = models.CharField(verbose_name=_("Alternative text of image"), max_length=255, help_text=_('In case image is not displayed due to slow internet connection, what should be displayed instead of this image as text. Text should describe what kind of image has to be displayed. It\'s important for SEO.'))
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = _("Product Image")
		verbose_name_plural = _("Product Images")

	def __str__(self):
		return f"{self.item}"

	def image_tag(self):
		if self.image:
			return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
		else:
			return 'No image found'
	image_tag.short_description = 'Image'


	def save(self, *args, **kwargs):
		img = PillowImage.open(self.image)
		# Resize image
		output_size = (800, 800)
		img.thumbnail(output_size)

		# Save the resized image to a BytesIO buffer
		output_buffer = BytesIO()
		img.save(output_buffer, format='WebP')
		output_buffer.seek(0)

		# Generate a unique name for the image
		random_string = get_random_string(length=8)
		timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
		filename = f'{random_string}_{timestamp}.webp'

		# Save the buffer content to the image field with the unique filename
		self.image.save(filename, ContentFile(output_buffer.read()), save=False)

		super().save(*args, **kwargs)
