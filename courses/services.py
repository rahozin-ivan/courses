import channels.layers
from asgiref.sync import async_to_sync


def send_mark_to_user(user, mark):
    channel_layer = channels.layers.get_channel_layer()

    async_to_sync(channel_layer.group_send)(f'User_{user.uuid}', {"type": "send.mark",
                                                                  "content": f'You have mark: {mark}'})
