import json
from enum import Enum

import aio_pika
from core.config import settings


# =========================================================
# RabbitMQ Connection (ASYNC)
# =========================================================
# WHY?
# - Used for event-driven architecture
# - Decouples microservices (auth → notification)
# - Ensures reliable message delivery
# =========================================================

# connection = None
# channel = None


# async def connect_rabbitmq():
#     """
#     Establish connection with RabbitMQ server
#     Call this on application startup
#     """

#     global connection, channel

#     # Create connection
#     connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

#     # Create channel (used to send/receive messages)
#     channel = await connection.channel()

#     print("✅✅✅ RabbitMQ connected successfully")


# async def close_rabbitmq():
#     """
#     Close connection safely on app shutdown
#     """

#     global connection

#     if connection:
#         await connection.close()
#         print("❌ RabbitMQ connection closed")

class RabbitMQ:
    def __init__(self):
        self.connection = None
        self.channel = None
        self._exchanges: dict[str, aio_pika.Exchange] = {}

    # =========================================================
    # CONNECT
    # =========================================================
    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            settings.RABBITMQ_URL
        )

        # Use publisher confirms so we get broker acks.
        # Do NOT raise on unroutable messages: in microservice setups the
        # consumer queues may not be declared/bound yet during deploys.
        self.channel = await self.connection.channel(
            publisher_confirms=True,
        )

        # declare exchanges (like NestJS module)
        self._exchanges["notifications.exchange"] = await self.channel.declare_exchange(
            "notifications.exchange",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        self._exchanges["app.events"] = await self.channel.declare_exchange(
            "app.events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        print("✅ RabbitMQ connected + exchanges created")

    # =========================================================
    # PUBLISH MESSAGE
    # =========================================================
    async def publish(self, exchange_name: str, routing_key: str, message: dict):
        if not self.channel or not self.connection:
            raise RuntimeError("RabbitMQ is not connected")

        exchange = self._exchanges.get(exchange_name)
        if exchange is None:
            # Fallback: create a lightweight exchange handle (no extra network calls
            # beyond what aio-pika needs for the channel).
            exchange = await self.channel.get_exchange(exchange_name)
            self._exchanges[exchange_name] = exchange

        await exchange.publish(
            aio_pika.Message(
                # Important for cross-service contracts: ship real JSON bytes.
                body=json.dumps(
                    message,
                    # For microservice contracts: encode Enums as their `.value`.
                    default=lambda obj: obj.value if isinstance(obj, Enum) else str(obj),
                    separators=(",", ":"),
                ).encode("utf-8"),
                content_type="application/json",
                content_encoding="utf-8",
                # Persist messages to survive broker restarts (requires durable queues on the consumer).
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
            mandatory=False,
        )

    # =========================================================
    # CLOSE
    # =========================================================
    async def close(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
            print("❌ RabbitMQ closed")