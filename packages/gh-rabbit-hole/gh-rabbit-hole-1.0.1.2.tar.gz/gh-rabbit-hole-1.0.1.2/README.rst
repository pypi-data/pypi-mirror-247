Libreria RabbitHole
===================

AsyncioRabbitManager
--------------------

Panoramica AsyncioRabbitManager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RabbitManager è una classe Python che facilita la gestione e
l’interazione con un server RabbitMQ. Fornisce funzionalità per la
configurazione di code e scambi, l’invio e la ricezione di messaggi, e
la gestione dinamica delle risorse su RabbitMQ.

Requisiti (AsyncioRabbitManager)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Python 3.6+
-  pika 1.1.0+
-  asyncio

Installazione (AsyncioRabbitManager)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assicurati di avere Python installato sul tuo sistema. Inoltre, è
necessario installare le librerie ``pika`` e ``asyncio``. Puoi
installarle usando pip:

.. code:: bash

   pip install pika asyncio

Utilizzo (AsyncioRabbitManager)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creazione dell’istanza AsyncRabbitManager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per utilizzare la classe RabbitManager, è necessario prima crearne
un’istanza. L’istanza richiede i dettagli della connessione al server
RabbitMQ, come l’URL AMQP, il nome della coda di invio e di ascolto, e
il nome dello scambio:

.. code:: python

   from rabbit_manager import RabbitManager
   amqp_url = 'amqp://guest:guest@localhost:5672/'
   sending_queue = 'test_queue'
   listening_queue = 'test_queue'
   sending_exchange = 'test_exchange'

   rabbit_manager = RabbitManager(amqp_url, sending_queue, listening_queue, sending_exchange)

Connessione al Server RabbitMQ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per connettersi al server RabbitMQ, usa il metodo ``connect``:

.. code:: python

   import asyncio

   loop = asyncio.get_event_loop()
   loop.run_until_complete(rabbit_manager.connect())

Invio di Messaggi (AsyncioRabbitManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per inviare messaggi, utilizza il metodo ``send_message``. Puoi
specificare se inviare il messaggio a una coda o a uno scambio:

.. code:: python

   message = {"key": "value"}
   routing_key = 'test_routing_key'

   loop.run_until_complete(rabbit_manager.send_message(message, routing_key=routing_key))

Ricezione di Messaggi (AsyncioRabbitManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per ascoltare i messaggi in arrivo, assicurati di definire una callback
e di avviare il processo di ascolto:

.. code:: python

   def on_message_callback(channel, method, properties, body):
       print("Messaggio ricevuto:", body)

   rabbit_manager.on_message_callback = on_message_callback
   rabbit_manager.start_listening()

Chiusura della Connessione (AsyncioRabbitManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per assicurare una chiusura pulita e ordinata della connessione con il
server RabbitMQ, è importante chiudere correttamente la connessione e le
risorse associate. La classe ``RabbitManager`` fornisce un metodo
``close_connection`` per questo scopo. Quando si chiama questo metodo,
viene inviato un comando di chiusura al server RabbitMQ e vengono
rilasciate tutte le risorse di rete e di sistema associate alla
connessione.

È buona pratica chiudere la connessione quando il tuo programma ha
finito di utilizzare RabbitMQ o sta per terminare. Questo aiuta a
prevenire perdite di risorse e assicura che la coda e lo scambio non
rimangano in uno stato inconsistente. Ecco come puoi chiudere la
connessione:

.. code:: python

   import asyncio
   # Crea un'istanza della classe RabbitManager
   rabbit_manager = RabbitManager(amqp_url, sending_queue, listening_queue, sending_exchange)

   async def manage_rabbit():
       # Connettiti a RabbitMQ
       await rabbit_manager.connect()

       # Esegui le operazioni desiderate con RabbitMQ...

       # Chiudi la connessione quando hai finito
       await rabbit_manager.close_connection()

   # Esegui la routine di gestione RabbitMQ
   loop = asyncio.get_event_loop()
   loop.run_until_complete(manage_rabbit())

Nell’esempio sopra, ``manage_rabbit`` è una coroutine asincrona che
gestisce il ciclo di vita della connessione RabbitMQ. Dopo aver
completato tutte le operazioni necessarie, chiama
``rabbit_manager.close_connection()`` per chiudere in modo sicuro la
connessione. Ricorda che è importante utilizzare ``asyncio`` per
eseguire queste operazioni in quanto la classe ``RabbitManager`` è
progettata per funzionare in modo asincrono.

RabbitManager
-------------

Panoramica (RabbitManager)
~~~~~~~~~~~~~~~~~~~~~~~~~~

La classe ``RabbitManager`` è progettata per facilitare la gestione e
l’interazione con un server RabbitMQ. Offre funzionalità per configurare
code e scambi, inviare e ricevere messaggi e gestire dinamicamente le
risorse su RabbitMQ.

Requisiti (RabbitManager)
~~~~~~~~~~~~~~~~~~~~~~~~~

-  Python 3.6+
-  pika
-  requests

Installazione (RabbitManager)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assicurati di avere Python installato sul tuo sistema. È inoltre
necessario installare le librerie ``pika`` e ``requests`` se non sono
già presenti. Queste possono essere installate usando pip:

.. code:: bash

   pip install pika requests

Utilizzo (RabbitManager)
~~~~~~~~~~~~~~~~~~~~~~~~

Inizializzazione (RabbitManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per utilizzare la classe ``RabbitManager``, inizializzala con i dettagli
della connessione al server RabbitMQ, come il nome della coda di invio e
di ascolto, lo scambio e le configurazioni specifiche:

.. code:: python

   from rabbit_manager import RabbitManager
   from rabbit_config import RabbitConfig

   # Configurazione per RabbitMQ
   rabbit_config = RabbitConfig({
       "rabbit_server": "localhost",
       "rabbit_port": 5672,
       "rabbit_credentials": ("guest", "guest")
   })

   rabbit_manager = RabbitManager(
       sending_queue="my_sending_queue",
       listening_queue="my_listening_queue",
       sending_exchange={"name": "my_exchange", "type": "direct"},
       config=rabbit_config
   )

Connessione (RabbitManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per connetterti al server RabbitMQ e configurare le code e gli scambi:

.. code:: python

   rabbit_manager.connect()

Invio di Messaggi (RabbitManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per inviare messaggi a una coda o a uno scambio:

.. code:: python

   rabbit_manager.send_message("Il mio messaggio", to_exchange=True, routing_key="my_routing_key")

Ricezione di Messaggi (RabbitManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per ascoltare i messaggi in arrivo:

.. code:: python

   def my_message_callback(channel, method, properties, body):
       print("Messaggio ricevuto:", body)

   rabbit_manager.on_message_callback = my_message_callback
   rabbit_manager.start_listening()

Rimozione di Code o Scambi (RabbitManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per rimuovere una coda o uno scambio:

.. code:: python

   rabbit_manager.remove_queue("my_queue")
   rabbit_manager.remove_exchange("my_exchange")

Arresto dell’Ascolto e Chiusura della Connessione (RabbitManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per fermare l’ascolto dei messaggi e chiudere la connessione:

.. code:: python

   rabbit_manager.stop_listening()
   rabbit_manager.connection.close()

ConfigFileManager and RabbitConfig
----------------------------------

Panoramica (Configurazione)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le classi ``ConfigFileManager`` e ``RabbitConfig`` forniscono una
struttura per gestire la configurazione di un’applicazione che
interagisce con RabbitMQ. ``ConfigFileManager`` gestisce il salvataggio
e il caricamento di configurazioni da file, mentre ``RabbitConfig``
utilizza ``ConfigFileManager`` per gestire specifiche configurazioni
RabbitMQ.

Requisiti (Configurazione)
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Python 3.6+
-  json
-  os

Utilizzo (Configurazione)
~~~~~~~~~~~~~~~~~~~~~~~~~

ConfigFileManager
^^^^^^^^^^^^^^^^^

Questa classe gestisce file di configurazione in formato JSON. Permette
di caricare, salvare e assicurarsi che la directory dei file di
configurazione esista.

Esempio di Utilizzo (ConfigFileManager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from config_file_manager import ConfigFileManager
   # Crea un'istanza di ConfigFileManager
   config_manager = ConfigFileManager("config_directory", "config_file.json")

   # Carica la configurazione
   config = config_manager.load()

   # Salva una nuova configurazione
   new_config = {"chiave": "valore"}
   config_manager.save(new_config)

Esempio di file di config
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: json

   {
       "rabbit_server": "localhost",
       "rabbit_port": 5672,
       "rabbit_credentials": [
           "guest",
           "guest"
       ],
       "rabbit_queues": [
           "test1_queue",
           "test2_queue",
       ],
       "rabbit_exchanges": [
           {
               "name": "test1_exchange",
               "type": "fanout"
           },
           {
               "name": "test2_ready_exchange",
               "type": "fanout"
           },
       ]
   }

Nell’esempio le voci minime necessarie per il file di configurazione

RabbitConfig
^^^^^^^^^^^^

Gestisce la configurazione specifica per RabbitMQ, caricando valori
predefiniti se necessario e validando i dati.

Esempio di Utilizzo (Configurazione)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from rabbit_config import RabbitConfig
   # Assumi che config_manager sia un'istanza di ConfigFileManager
   rabbit_config = RabbitConfig(config_manager)

   # Ottieni la configurazione corrente
   current_config = rabbit_config.get_config()

   # Aggiorna la configurazione
   new_config = {"rabbit_server": "new.server.address"}
   rabbit_config.update_config(new_config)

   # Salva la configurazione in un percorso specifico
   rabbit_config.save_config("path/to/save/config.json")
