# Generated by Django 5.0.4 on 2024-11-24 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_rename_name_category_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required', max_length=255, verbose_name='Collection Name')),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True, verbose_name='Collection Safe URL')),
            ],
            options={
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='featured_category',
        ),
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.ManyToManyField(related_name='posts', to='store.collection'),
        ),
        migrations.DeleteModel(
            name='FeaturedCategory',
        ),
    ]
