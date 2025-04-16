import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from crm.models import ServiceRequestImage


@receiver(pre_delete, sender=ServiceRequestImage)
def delete_imagekit_files(sender, instance, **kwargs):
    """Удаляет thumbnail перед удалением файла ServiceRequestImage"""
    if hasattr(instance, "thumbnail"):
        try:
            thumbnail_path = instance.thumbnail.path
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
        except (ValueError, AttributeError):
            # Если файл не существует или другие ошибки
            pass