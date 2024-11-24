from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import CategoryMedia, Category, ProductMedia, Product
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=CategoryMedia)
def category_image_saved(sender, instance, created, **kwargs):
    """
    Signal to clear cache when a CategoryMedia instance is created or updated
    """
    # Check if this media belongs to a category
    if instance.content_type == ContentType.objects.get_for_model(Category):
        try:
            category = Category.objects.get(id=instance.object_id)
            # Clear the cache for this category's images
            cache.delete(f'category_images_{category.id}')
        except Category.DoesNotExist:
            pass

@receiver(post_delete, sender=CategoryMedia)
def category_image_deleted(sender, instance, **kwargs):
    """
    Signal to clear cache when a CategoryMedia instance is deleted
    """
    # Check if this media belongs to a category
    if instance.content_type == ContentType.objects.get_for_model(Category):
        try:
            category = Category.objects.get(id=instance.object_id)
            # Clear the cache for this category's images
            cache.delete(f'category_images_{category.id}')
        except Category.DoesNotExist:
            pass


@receiver(post_save, sender=ProductMedia)
def product_image_saved(sender, instance, created, **kwargs):
    """
    Signal to clear cache when a ProductMedia instance is created or updated
    """
    if instance.content_type == ContentType.objects.get_for_model(Product):
        try:
            product = Product.objects.get(id=instance.object_id)
            # Clear both the images list cache and first image cache
            cache.delete(f'product_images_{product.id}')
        except Product.DoesNotExist:
            pass

@receiver(post_delete, sender=ProductMedia)
def product_image_deleted(sender, instance, **kwargs):
    """
    Signal to clear cache when a ProductMedia instance is deleted
    """
    if instance.content_type == ContentType.objects.get_for_model(Product):
        try:
            product = Product.objects.get(id=instance.object_id)
            # Clear both the images list cache and first image cache
            cache.delete(f'product_images_{product.id}')
        except Product.DoesNotExist:
            pass