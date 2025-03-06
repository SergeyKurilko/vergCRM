from django.db.models.signals import post_save
from django.dispatch import receiver
from crm.models import CostPriceCase, ServiceRequest

@receiver(post_save, sender=CostPriceCase)
def cost_price_case_post_save(sender, instance, created, **kwargs):
    if created:
        # Все кейсы переводим в режим current = False, кроме созданного.
        # Он default=True
        (CostPriceCase.objects.filter(
                service_request_id=instance.service_request_id
            )
            .exclude(id=instance.id)
            .update(current=False)
        )

        # Сохраняем в поле cost_price у instance.service_request значение instance.sum
        ServiceRequest.objects.filter(id=instance.service_request_id).update(cost_price=instance.sum)