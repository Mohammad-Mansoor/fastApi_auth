from core.rabbitmq import RabbitMQ
from .notifications_schemas import SendNotificationDto


class NotificationProducerService:
    def __init__(self, rabbitmq: RabbitMQ):
        self.rabbitmq = rabbitmq

    async def send(self, dto: SendNotificationDto):

        channel_map = {
            "email": "notification.email",
            "whatsapp": "notification.whatsapp",
            "telegram": "notification.telegram",
            "inapp": "notification.inapp",
            "socket": "notification.socket",
        }

        for channel in dto.channels:
            routing_key = channel_map.get(channel)

            if routing_key:
                await self.rabbitmq.publish(
                    "notifications.exchange",
                    routing_key,
                    {
                        "type": dto.type,
                        "payload": dto.payload,
                    }
                )