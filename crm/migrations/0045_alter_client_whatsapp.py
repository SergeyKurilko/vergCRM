# Generated by Django 5.1.6 on 2025-05-03 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0044_alter_client_phone_2_alter_userprofile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=16, verbose_name='Whatsapp'),
        ),
    ]
