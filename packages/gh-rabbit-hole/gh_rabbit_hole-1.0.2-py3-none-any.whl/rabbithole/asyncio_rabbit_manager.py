import asyncio
import pika
import json
import logging
from pika.adapters.asyncio_connection import AsyncioConnection


class AsyncioRabbitManager:
    """
    La classe AsyncioRabbitManager fornisce un'interfaccia asincrona per connettersi e interagire
    con RabbitMQ utilizzando Python e asyncio. Progettata per applicazioni che richiedono un'elaborazione
    reattiva e non bloccante, questa classe gestisce la connessione a RabbitMQ, l'invio e la ricezione di messaggi,
    e la dichiarazione di scambi e code, tutto in modo asincrono.

    Principali caratteristiche:
    - Connessione Asincrona: Stabilisce connessioni non bloccanti a RabbitMQ, permettendo al resto dell'applicazione
      di continuare l'esecuzione mentre gestisce le operazioni di rete in background.
    - Gestione dei Canali: Apertura e configurazione dei canali RabbitMQ per inviare e ricevere messaggi.
    - Invio e Ricezione di Messaggi: Supporta l'invio di messaggi a code o scambi e la configurazione di callback
      asincrone per la gestione di messaggi in arrivo.
    - Integrazione con Asyncio: Costruita attorno alle primitive di asyncio, facilita l'integrazione con altre
      operazioni asincrone e il loop di eventi.
    - Logging Avanzato: Utilizza un sistema di logging personalizzabile per monitorare le attività e diagnosticare
      rapidamente eventuali problemi.

    Utilizzo:
    Ideale per applicazioni basate su asyncio che richiedono una comunicazione efficace e asincrona con RabbitMQ.
    È particolarmente utile in contesti in cui le prestazioni e la reattività sono critiche, come nei microservizi,
    nei bot, o in sistemi di elaborazione di dati in tempo reale.

    Args:
        amqp_url (str): URL per la connessione a RabbitMQ.
        sending_queue (str): Nome della coda per l'invio dei messaggi.
        listening_queue (str): Nome della coda per la ricezione dei messaggi.
        sending_exchange (str): Nome dello scambio usato per inviare i messaggi.
        logger (logging.Logger): Logger per registrare attività e errori.
        on_message_callback (Callable, optional): Callback asincrona invocata alla ricezione di un messaggio.
    """

    def __init__(
        self,
        amqp_url: str,
        sending_queue: str,
        listening_queue: str,
        sending_exchange: str,
        logger: logging.Logger,
        on_message_callback=None,
    ):
        self.amqp_url = amqp_url
        self.sending_queue = sending_queue
        self.listening_queue = listening_queue
        self.sending_exchange = sending_exchange
        self.on_message_callback = on_message_callback
        self.logger = logger
        self.connection = None
        self.channel: pika.channel.Channel = None
        self.__connection_opened_event = asyncio.Event()
        self.__channel_opened_event = asyncio.Event()
        self.__sending_queue_declared_event = asyncio.Event()
        self.__listening_queue_declared_event = asyncio.Event()
        self.__exchange_declared_event = asyncio.Event()

    async def connect(self):
        """
        Stabilisce una connessione asincrona con RabbitMQ e prepara il canale e lo scambio.
        """
        connection_parameters = pika.URLParameters(self.amqp_url)
        self.connection: AsyncioConnection = AsyncioConnection(
            parameters=connection_parameters,
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
        )
        await self.__connection_opened_event.wait()
        await self.__channel_opened_event.wait()
        await self.__sending_queue_declared_event.wait()
        await self.__listening_queue_declared_event.wait()
        await self.__exchange_declared_event.wait()
        # self.__connection_opened_event.clear()

    def on_connection_open(self, connection):
        """
        Callback invocata quando la connessione a RabbitMQ viene aperta.

        Args:
            connection: Connessione a RabbitMQ.
        """
        self.logger.info("Connection opened")
        self.connection.channel(on_open_callback=self.on_channel_open)
        self.__connection_opened_event.set()

        # self.__channel_opened_event.clear()

    def on_connection_open_error(self, connection, error):
        """
        Callback invocata in caso di errore durante l'apertura della connessione.

        Args:
            connection: Connessione a RabbitMQ.
            error: Oggetto errore che descrive il problema riscontrato.
        """
        self.logger.error("Connection open error: %s", error)
        self.__connection_opened_event.set()

    def on_channel_open(self, channel):
        """
        Callback invocata quando un canale RabbitMQ viene aperto.

        Args:
            channel: Canale RabbitMQ aperto.
        """
        self.logger.info("Channel opened")
        self.channel: pika.channel.Channel = channel
        self.channel.exchange_declare(
            exchange=self.sending_exchange,
            exchange_type="direct",
            callback=self.on_exchange_declareok,
        )
        self.channel.queue_declare(
            queue=self.sending_queue,
            callback=self.on_sending_queue_declareok,
            durable=True,
        )
        self.channel.queue_declare(
            queue=self.listening_queue,
            callback=self.on_listening_queue_declareok,
            durable=True,
        )
        self.__channel_opened_event.set()

    def on_exchange_declareok(self, frame):
        """
        Callback invocata dopo la dichiarazione dello scambio.

        Args:
            frame: Frame di risposta di RabbitMQ.
        """
        self.logger.info(f"[x] {self.sending_exchange} declared")
        self.__exchange_declared_event.set()

    def on_listening_queue_declareok(self, frame):
        """
        Callback invocata dopo la dichiarazione della coda di ascolto.

        Args:
            frame: Frame di risposta di RabbitMQ.
        """
        self.logger.info(f"[x] {self.listening_queue} declared")
        if self.listening_queue:
            self.channel.basic_consume(
                queue=self.listening_queue,
                on_message_callback=self.on_message_wrapper,
                auto_ack=True,
            )
        self.__listening_queue_declared_event.set()

    def on_sending_queue_declareok(self, frame):
        """
        Callback invocata dopo la dichiarazione della coda di invio.

        Args:
            frame: Frame di risposta di RabbitMQ.
        """
        self.logger.info(f"[x] {self.sending_queue} declared")
        self.__sending_queue_declared_event.set()

    def on_message_wrapper(self, channel, method, properties, body):
        """
        Wrapper per la callback on_message, crea un task asincrono.

        Args:
            channel: Canale RabbitMQ.
            method: Metodo di messaggistica RabbitMQ.
            properties: Proprietà del messaggio RabbitMQ.
            body: Corpo del messaggio.
        """
        asyncio.create_task(self.on_message(channel, method, properties, body))

    async def on_message(self, channel, method, properties, body):
        """
        Callback asincrona per la gestione dei messaggi ricevuti.

        Args:
            channel: Canale RabbitMQ.
            method: Metodo di messaggistica RabbitMQ.
            properties: Proprietà del messaggio RabbitMQ.
            body: Corpo del messaggio.
        """
        if self.on_message_callback:
            await self.on_message_callback(channel, method, properties, body)
        else:
            self.logger.info(f"Received message: {body} on channel: {channel}")

    def send_message(self, message, routing_key="", to_exchange=False):
        """
        Invia un messaggio a RabbitMQ.

        Args:
            message: Il messaggio da inviare.
            routing_key (str, optional): Chiave di routing per il messaggio.
            to_exchange (bool, optional): Se inviare il messaggio allo scambio.
        """
        if not self.connection or not self.connection.is_open:
            raise ConnectionError("Connection not open")
        message = json.dumps(message)
        routing_key = (
            self.sending_queue
            if routing_key is None or routing_key == ""
            else routing_key
        )
        properties = pika.BasicProperties(
            app_id="rabbit-hole", content_type="application/json"
        )
        exchange = self.sending_exchange if to_exchange else ""
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
            properties=properties,
        )
        self.logger.info("Message sent to %s: %s", routing_key, message)

    async def close_connection(self):
        """
        Chiude la connessione con RabbitMQ in modo asincrono.
        """
        if self.connection and self.connection.is_open:
            await self.connection.close()


if __name__ == "__main__":
    import aioconsole

    LOG_FORMAT = (
        "\033[1;31m%(levelname)s\033[1;0m "  # Rosso per il livello di log
        "\033[1;34m%(asctime)s\033[1;0m "  # Blu per il timestamp
        "\033[1;32m%(name)-30s\033[1;0m "  # Verde per il nome del logger
        "\033[1;35m%(funcName)-35s\033[1;0m "  # Viola per il nome della funzione
        "\033[1;33m%(lineno)-5d\033[1;0m: "  # Giallo per il numero di riga
        "%(message)s"  # Testo normale per il messaggio
    )
    logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT)
    LOGGER = logging.getLogger("RabbitManager")
    LOGGER.setLevel(logging.INFO)

    async def message_received(channel, method, properties, body):
        LOGGER.info("Message received: %s", body)

    async def main():
        # loop = asyncio.get_event_loop()
        amqp_url = "amqp://guest:guest@localhost:5672/"
        rabbit_manager = AsyncioRabbitManager(
            amqp_url=amqp_url,
            sending_queue="frame_ready_queue",
            listening_queue="commands_queue",
            sending_exchange="test_exchange",
            logger=LOGGER,
            on_message_callback=message_received,
        )
        await rabbit_manager.connect()
        # await asyncio.sleep(2)
        while True:
            message = await aioconsole.ainput("Inserisci un messaggio: ")
            rabbit_manager.send_message({"message": message}, routing_key="")

        await rabbit_manager.close_connection()

    # Altre operazioni asincrone possono essere aggiunte qui
    asyncio.run(main())
