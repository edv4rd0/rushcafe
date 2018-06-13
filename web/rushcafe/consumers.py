import json

from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from rushcafe.dialogflow import CafeDialogflow
from rushcafe.models import Message


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        if self.scope["session"].session_key:
            messages = Message.objects.filter(
                user_session_id=self.scope["session"].session_key
            ).order_by('-time_stamp')[:10]

            for message in reversed(messages):
                    self.send(text_data=json.dumps({
                        'message': message.message,
                        'is_bot': message.is_bot
                    }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        Message.objects.create(
            user_session_id=self.scope["session"].session_key,
            message=message
        )

        dialogflow = CafeDialogflow(**settings.DIALOGFLOW)
        response = dialogflow.text_request(message)

        self.send(text_data=json.dumps({
            'message': response,
            'is_bot': True,
        }))

        Message.objects.create(
            user_session_id=self.scope["session"].session_key,
            message=response,
            is_bot=True
        )
