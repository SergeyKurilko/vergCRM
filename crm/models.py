from django.db import models
from django.urls import reverse

from crm.utils import service_request_image_path
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=15, verbose_name="telegram", blank=True)
    phone_number = models.CharField(max_length=15, verbose_name="телефон", blank=True)

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"

    class Meta:
        verbose_name = "Профиль менеджера"
        verbose_name_plural = "Профили менеджеров"


class Client(models.Model):
    """
    Описывает объект Client
    """
    name = models.CharField(max_length=255,
                            verbose_name="ФИО Клиента")
    phone = models.CharField(max_length=15,
                             verbose_name="Телефон")
    phone_2 = models.CharField(max_length=15,
                               verbose_name="Второй телефон",
                               blank=True)
    whatsapp = models.CharField(max_length=15,
                                verbose_name="Whatsapp",
                                blank=True)
    telegram = models.CharField(max_length=55,
                                verbose_name="telegram",
                                blank=True)
    email = models.EmailField(verbose_name="email", blank=True)
    manager = models.ForeignKey(to=User,
                                on_delete=models.SET_NULL,
                                related_name="clients",
                                null=True, blank=True)

    def __str__(self):
        return f"Клиент: {self.name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["-id"]



class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'), # TODO: убрать этот статус
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('canceled', 'Отменена'),
        ('archive', 'В архиве'), # TODO: убрать этот статус
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE,
                               verbose_name="Клиент", related_name="service_requests")
    address = models.TextField(verbose_name="Адрес", blank=True)
    description = models.TextField(verbose_name="Подробное описание заявки")
    cost_price = models.IntegerField(verbose_name="Общая себестоимость",
                                     blank=True,
                                     null=True,
                                     default=0
                                     )
    total_price = models.PositiveIntegerField(verbose_name="Общая стоимость",
                                              blank=True,
                                              null=True,
                                              default=0)
    manager = models.ForeignKey(to=User,
                                on_delete=models.SET_NULL,
                                related_name="service_requests",
                                null=True, blank=True)
    service = models.ForeignKey(to="Service",
                                on_delete=models.SET_NULL,
                                related_name="service_requests",
                                null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default='in_progress', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Дата и время изменения")

    def __str__(self):
        return f"Сделка №{self.pk} для клиента {self.client.name}."

    def get_absolute_url(self):
        return reverse("crm:service_request_detail", args=[self.pk])

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-updated_at"]


class CostPriceCase(models.Model):
    """
    Кейс себестоимости
    """
    title = models.CharField(
        max_length=255,
        verbose_name="Название кейса",
        blank=True,
        null=True)
    sum = models.IntegerField(
        verbose_name="Общая себестоимость кейса",
        blank=True,
        null=True,
        default=0
    )
    current = models.BooleanField(
        verbose_name="Актуальный",
        default=False
    )
    service_request = models.ForeignKey(
        to="ServiceRequest",
        related_name="coast_price_cases",
        verbose_name="Заявка",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.pk} Кейс себестоимости для заявки {self.service_request.id}. Прайс: {self.sum}. Выбран: {self.current}"

    class Meta:
        verbose_name = "Кейс себестоимости"
        verbose_name_plural = "Кейс себестоимости"


class PartOfCostPriceCase(models.Model):
    """
    Одна составная часть кейса себестоимости
    """
    title = models.CharField(
        max_length=300,
        verbose_name="Название"
    )
    sum = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Сумма"
    )
    cost_price_case = models.ForeignKey(
        to="CostPriceCase",
        related_name="parts",
        verbose_name="Часть себестоимости",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Часть кейса себестоимости"
        verbose_name_plural = "Части кейсов себестоимости"


class Service(models.Model):
    """
    Услуга для заявки
    """
    title = models.CharField(max_length=350, verbose_name="Услуга")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class NoteForServiceRequest(models.Model):
    text = models.TextField(verbose_name="Текст заметки")
    service_request = models.ForeignKey(to=ServiceRequest,
                                        on_delete=models.CASCADE,
                                        related_name="notes")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Дата и время изменения")



    def __str__(self):
        return f"Заметка №{self.id} к заявке №{self.service_request}."

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        ordering = ["-updated_at"]


class ImageForServiceRequest(models.Model):
    image = models.ImageField(verbose_name="Изображение к заявке", upload_to=service_request_image_path)
    service_request = models.ForeignKey(to=ServiceRequest,
                                        on_delete=models.CASCADE,
                                        related_name="images")

    class Meta:
        verbose_name = "Изображение для заявки"
        verbose_name_plural = "Изображения для заявок"


class Comment(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE,
                                related_name='comments',
                                verbose_name="Заявка")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий к заявке #{self.request.id}"

    class Meta:
        verbose_name = "Комментарий к заявке"
        verbose_name_plural = "Комментарии к заявкам"


class Task(models.Model):
    """
    Описывает объект Task. Опционально может иметь FK на ServiceRequest
    """
    title = models.CharField(verbose_name="Название задачи", max_length=255)
    text = models.TextField(verbose_name="Текст задачи")

    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE,
                                        related_name='tasks',
                                        verbose_name="Заявка",
                                        null=True, blank=True)

    manager = models.ForeignKey(User, on_delete=models.CASCADE,
                                        related_name='tasks',
                                        verbose_name="Менеджер")

    must_be_completed_by = models.DateTimeField(verbose_name="Должна быть выполнена до")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата создания")

    is_completed = models.BooleanField(default=False, verbose_name="Выполнено")
    reminder = models.BooleanField(default=False, verbose_name="Напоминание")
    expired = models.BooleanField(default=False, verbose_name="Просрочена")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-expired", "must_be_completed_by"]

