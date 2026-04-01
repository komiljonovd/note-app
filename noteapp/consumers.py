# consumers.py

from channels.generic.websocket import WebsocketConsumer
import json
from .models import Document
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class DocumentListConsumer(WebsocketConsumer):

    def connect(self):
        self.group_name = "documents"

        # подключаемся к группе
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

        # отправляем ВСЕ документы
        documents = list(
            Document.objects.all().values(
                'id', 'title', 'content'
            )
        )

        self.send(text_data=json.dumps({
            "type": "init",
            "documents": documents
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # 🔥 событие от group_send
    def new_document(self, event):
        self.send(text_data=json.dumps({
            "type": "new_document",
            "document": event["document"]
        }))
    
    def update_document(self, event):
        self.send(text_data=json.dumps({
        "type": "update_document",
        "document": event["document"]
    }))


    def delete_document(self, event):
        self.send(text_data=json.dumps({
            "type": "delete_document",
            "document_id": event["document_id"]
        }))