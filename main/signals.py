from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver

@receiver(pre_save, sender=User)
def ensure_unique_email(sender, instance, **kwargs):
    if User.objects.filter(email=instance.email).exclude(pk=instance.pk).exists():
        raise ValidationError('The email already exists in the database.')