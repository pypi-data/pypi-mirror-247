import asyncio
import pika
import json
import logging
from pika.adapters.asyncio_connection import AsyncioConnection

LOGGER = logging.getLogger(__name__)


class AsyncioRabbitManager:
    """
    Gestisce la connessione e l'interazione con un server RabbitMQ in modo asincrono.
    """

    def __init__(
        self,
        amqp_url,
        sending_queue,
        listening_queue,
        sending_exchange,
        on_message_callback=None,
    ):
        self.amqp_url = amqp_url
        self.sending_queue = sending_queue
        self.listening_queue = listening_queue
        self.sending_exchange = sending_exchange
        self.on_message_callback = on_message_callback

        self.connection = None
        self.channel = None

    async def connect(self):
        connection_parameters = pika.URLParameters(self.amqp_url)
        self.connection = AsyncioConnection(
            parameters=connection_parameters, on_open_callback=self.on_connection_open
        )
        await self.connection.connect()

    def on_connection_open(self, connection):
        LOGGER.info("Connection opened")
        self.connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        LOGGER.info("Channel opened")
        self.channel = channel
        self.channel.exchange_declare(
            exchange=self.sending_exchange,
            exchange_type="direct",
            callback=self.on_exchange_declareok,
        )
        self.channel.queue_declare(
            queue=self.sending_queue, callback=self.on_queue_declareok
        )
        self.channel.queue_declare(
            queue=self.listening_queue, callback=self.on_queue_declareok
        )

    def on_exchange_declareok(self, frame):
        LOGGER.info("Exchange declared")

    def on_queue_declareok(self, frame):
        LOGGER.info("Queue declared")
        if self.listening_queue:
            self.channel.basic_consume(
                queue=self.listening_queue,
                on_message_callback=self.on_message,
                auto_ack=True,
            )

    async def on_message(self, channel, method, properties, body):
        if self.on_message_callback:
            await self.on_message_callback(channel, method, properties, body)
        else:
            print("Nessuna callback definita per il messaggio ricevuto.")

    async def send_message(self, message, routing_key=""):
        if not self.connection or not self.connection.is_open:
            raise ConnectionError("Connection not open")
        message = json.dumps(message)

        self.channel.basic_publish(
            exchange=self.sending_exchange, routing_key=routing_key, body=message
        )

    async def close_connection(self):
        if self.connection and self.connection.is_open:
            await self.connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    amqp_url = "amqp://guest:guest@localhost:5672/"
    rabbit_manager = AsyncioRabbitManager(
        amqp_url, "test_queue", "test_queue", "test_exchange"
    )
    loop.run_until_complete(rabbit_manager.connect())
    # Altre operazioni asincrone possono essere aggiunte qui
