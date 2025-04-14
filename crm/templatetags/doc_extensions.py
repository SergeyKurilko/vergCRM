from django import template
from urllib.parse import unquote  # Добавляем декодирование URL

register = template.Library()

@register.filter
def get_file_extension(value: str):
    """Возвращает расширение файла"""
    extension = value.split(".")[-1]
    return extension.lower()

@register.filter
def get_document_name(value):
    """Извлекает имя файла из URL и декодирует русские символы."""
    filename = value.split('/')[-1]
    return unquote(filename)  # Декодируем %D0... в нормальные символы



