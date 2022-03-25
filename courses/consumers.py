from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class GetMarkConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        self.group_name = f'User_{user.uuid}'

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )

    def send_mark(self, message):
        self.send(message['content'])
