# Generated by Django 5.1.6 on 2025-02-26 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_rename_request_comment_service_request_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий к заявке', 'verbose_name_plural': 'Комментарии к заявкам'},
        ),
        migrations.AlterModelOptions(
            name='imageforservicerequest',
            options={'verbose_name': 'Изображение для заявки', 'verbose_name_plural': 'Изображения для заявок'},
        ),
        migrations.AlterModelOptions(
            name='servicerequest',
            options={'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
        migrations.AddField(
            model_name='task',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='Выполнено'),
        ),
    ]
