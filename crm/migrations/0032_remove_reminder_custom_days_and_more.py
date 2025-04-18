# Generated by Django 5.1.6 on 2025-03-26 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0031_alter_task_must_be_completed_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reminder',
            name='custom_days',
        ),
        migrations.RemoveField(
            model_name='reminder',
            name='custom_time',
        ),
        migrations.AddField(
            model_name='reminder',
            name='recurring_days',
            field=models.JSONField(blank=True, default=list, help_text="Дни недели, например ['mon', 'wed', 'fri']"),
        ),
        migrations.AddField(
            model_name='reminder',
            name='recurring_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reminder',
            name='scheduled_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='mode',
            field=models.CharField(choices=[('once', 'Разовое'), ('recurring', 'Повторяющееся')], max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='notifications',
            field=models.BooleanField(default=False, verbose_name='Оповещение о сроке выполнения'),
        ),
    ]
