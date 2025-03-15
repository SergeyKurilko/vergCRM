# Generated by Django 5.1.6 on 2025-03-15 11:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0024_remove_noteforservicerequest_be_completed_before_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-expired', 'must_be_completed_by'], 'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='crm.client', verbose_name='Клиент'),
        ),
    ]
