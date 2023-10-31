import hashlib
import random
import uuid

from core.utils.models import TimeStampedModel
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from users.tasks import send_otp_email


class VerificationCode(TimeStampedModel):
    code = models.CharField(max_length=6,
                            default=random.randint(100000, 999999))
    email = models.EmailField(unique=True)
    hash = models.TextField()
    is_email_sent = models.BooleanField(default=False)

    def __str__(self):
        return (f'{self.email} {self.code}')


@receiver(pre_save, sender=VerificationCode)
def handle_pre_save_verification(sender, instance, *args, **kwargs):
    if instance.id is None:
        instance.hash = hashlib.sha512(
            f"{instance.email}{instance.code}".encode()).hexdigest()


@receiver(post_save, sender=VerificationCode)
def handle_post_save_verification(sender, instance, created, *args, **kwargs):
    if created or not instance.is_email_sent:
        send_otp_email(instance.id)


class Document(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='processing')
    document = models.FileField(null=True, blank=True)

    def __str__(self):
        return f'{self.model}: {self.uuid}'
