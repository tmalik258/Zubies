# Generated by Django 5.0.4 on 2024-09-18 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('D', 'Delivered'), ('P', 'In Process'), ('C', 'Is Cancelled')], default='P', max_length=2),
        ),
    ]
