# Generated by Django 5.1.6 on 2025-04-09 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0035_alter_task_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicerequest',
            options={'ordering': [models.Case(models.When(status='in_progress', then=models.Value(0)), models.When(status='completed', then=models.Value(1)), models.When(status='canceled', then=models.Value(2)), default=models.Value(3), output_field=models.IntegerField()), '-updated_at'], 'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['is_completed', 'expired', 'must_be_completed_by'], 'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='status',
            field=models.CharField(choices=[('in_progress', 'В работе'), ('completed', 'Завершена'), ('canceled', 'Отменена')], default='in_progress', max_length=15),
        ),
    ]
