# Generated by Django 5.1.6 on 2025-03-05 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0012_remove_servicerequest_cost_price_coastpricecase_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequest',
            name='cost_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Общая себестоимость'),
        ),
    ]
