# Generated by Django 5.1.6 on 2025-03-05 16:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_noteforservicerequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicerequest',
            name='cost_price',
        ),
        migrations.CreateModel(
            name='CoastPriceCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название кейса')),
                ('service_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coast_price_cases', to='crm.servicerequest', verbose_name='Заявка')),
            ],
            options={
                'verbose_name': 'Кейс себестоимости',
                'verbose_name_plural': 'Кейс себестоимости',
            },
        ),
        migrations.CreateModel(
            name='PartOfCoatPriceCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Название')),
                ('sum', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма')),
                ('coast_price_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='crm.coastpricecase', verbose_name='Часть себестоимости')),
            ],
            options={
                'verbose_name': 'Часть кейса себестоимости',
                'verbose_name_plural': 'Части кейсов себестоимости',
            },
        ),
    ]
