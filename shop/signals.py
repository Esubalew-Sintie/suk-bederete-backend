from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ShopRating

@receiver(post_save, sender=ShopRating)
def update_shop_rating_on_save(sender, instance, **kwargs):
    instance.shop.save()

@receiver(post_delete, sender=ShopRating)
def update_shop_rating_on_delete(sender, instance, **kwargs):
    instance.shop.save()
