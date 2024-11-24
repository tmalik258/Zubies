# Generated by Django 5.0.4 on 2024-11-24 20:51

from django.db import migrations, models
from decimal import Decimal, InvalidOperation

def convert_weight_to_decimal(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    for product in Product.objects.all():
        try:
            # Attempt to convert weight to Decimal
            product.weight = Decimal(product.weight) if product.weight not in [None, ''] else Decimal(0)
        except (InvalidOperation, ValueError, TypeError):
            # Handle invalid weight values (e.g. empty, None, or malformed values)
            product.weight = Decimal(0)  # Default to 0 if conversion fails
        product.save()



class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_remove_product_user_wishlist_product_wishlist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.DecimalField(default=Decimal('0'), max_digits=10, decimal_places=3, help_text='kg'),
        ),
        migrations.RunPython(convert_weight_to_decimal),
    ]
