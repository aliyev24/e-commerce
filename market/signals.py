from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models


@receiver(post_save, sender = models.User)
def create_cart(sender, instance,created, **kwargs):
    if created:
        models.Cart.objects.create(user=instance, is_active=True,total=0)
