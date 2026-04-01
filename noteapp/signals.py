from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Document
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# ➕ CREATE + ✏️ UPDATE
@receiver(post_save, sender=Document)
def document_saved(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    if created:
        event_type = "new_document"
    else:
        event_type = "update_document"

    async_to_sync(channel_layer.group_send)(
        "documents",
        {
            "type": event_type,
            "document": {
                "id": instance.id,
                "title": instance.title,
                "content": instance.content
            }
        }
    )


# ❌ DELETE
@receiver(post_delete, sender=Document)
def document_deleted(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "documents",
        {
            "type": "delete_document",
            "document_id": instance.id
        }
    )