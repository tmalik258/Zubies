# Generated by Django 5.0.4 on 2024-06-11 19:15

import django.db.models.deletion
import mptt.fields
import store.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required', max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Product Specification',
                'verbose_name_plural': 'Product Specifications',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required and unique', max_length=124, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Category Safe URL')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Required', max_length=255, unique=True)),
                ('regular_price', models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 99999999.99.'}}, help_text='Maximum 99999999.99', max_digits=10, verbose_name='Regular Price')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 99999999.99.'}}, help_text='Maximum 99999999.99', max_digits=10, null=True, verbose_name='Discount Price')),
                ('description', models.TextField(help_text='Required')),
                ('is_active', models.BooleanField(default=True, help_text='Change Product Visibility', verbose_name='Product Visibility')),
                ('in_stock', models.BooleanField(default=True)),
                ('weight', models.IntegerField(default=0)),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='store.category')),
                ('user_wishlist', models.ManyToManyField(blank=True, related_name='user_wishlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('-time_created',),
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=store.models.ProductMedia.directory_path, verbose_name='image')),
                ('alt_text', models.CharField(help_text="In case image is not displayed due to slow internet connection, what should be displayed instead of this image as text. Text should describe what kind of image has to be displayed. It's important for SEO.", max_length=255, verbose_name='Alternative text of image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='img', to='store.product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.CreateModel(
            name='ProductSpecificationValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(help_text='Product Specification Value (maximum of 255 characters)', max_length=255, verbose_name='value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specification', to='store.product')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productspecification')),
            ],
            options={
                'verbose_name': 'Product Specification Value',
                'verbose_name_plural': 'product Specification Values',
            },
        ),
    ]
