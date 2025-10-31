# cheques/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Cheque, ChequeAudit

@receiver(pre_save, sender=Cheque)
def create_audit(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        prev = Cheque.objects.get(pk=instance.pk)
    except Cheque.DoesNotExist:
        return
    if prev.status != instance.status:
        ChequeAudit.objects.create(
            cheque=instance,
            old_status=prev.status,
            new_status=instance.status,
            message=f"Status changed from {prev.status} → {instance.status}"
        )
