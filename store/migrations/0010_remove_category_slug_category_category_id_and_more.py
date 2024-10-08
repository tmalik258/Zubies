# Generated by Django 5.0.4 on 2024-09-07 10:29

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_productimage_alt_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.AddField(
            model_name='category',
            name='category_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Required and unique', max_length=124, verbose_name='Category Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.IntegerField(default=0, help_text='kg'),
        ),
    ]
