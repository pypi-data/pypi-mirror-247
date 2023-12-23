# log_messages.py


class RabbitLogMessages:
    GENERIC_ERROR = "Error: {}"

    # Costanti per i messaggi di log
    CONNECTION_OPENED = "Connection opened"
    CONNECTION_OPENED_DEBUG = "Connection opened: {}"
    CONNECTION_NOT_ESTABLISHED = "Connection not established"
    CONNECTION_CLOSED = "Connection closed: {}"
    CONNECTION_CLOSED_DEBUG = "Connection closed: {}"
    CONNECTION_NOT_OPEN_ERROR = "Connection not open"
    CONNECTION_OPEN_ERROR = "Connection open error: {}"
    CONNECTION_OPEN_ERROR_DEBUG = "Connection {connection} open error: {error}"
    CONNECTION_FAILED = "Failed to connect to RabbitMQ: {}"
    ATTEMPT_RECONNECT = (
        "Attempt to reconnect {attempts}/{max_attempts} in {delay} seconds..."
    )
    RECONNECT_FAILED = "Reached the maximum number of reconnection attempts ({})."
    CONNECTION_CLOSING_ERROR = "Error in closing connection: {}"
    CONNECTION_NOT_OPENED = "Connection not opened"

    CHANNEL_OPENED = "Channel opened"
    CHANNEL_OPENED_DEBUG = "Channel opened: {}"
    CHANNEL_OPEN_FAILED = "Failed to open channel: {}"
    CHANNEL_OPEN_ERROR = "Error in opening channel: {}"
    CHANNEL_OPEN_ERROR_DEBUG = "Channel {channel} open error: {error}"
    CHANNEL_CLOSED = "RabbitMQ channel closed."
    CHANNEL_CLOSING_ERROR = "Error in closing channel: {}"
    CHANNEL_NOT_OPENED = "Channel not opened"

    QUEUE_DECLARED = "[x] {} declared"
    QUEUE_DECLARED_DEBUG = "[x] {exchange} declared: {frame}"

    MESSAGE_RECEIVED = "Received message: {} on channel: {}"
    MESSAGE_RECEIVED_DEBUG = "Received message: {message} on channel: {channel}, method: {method}, properties: {properties}"
    MESSAGE_SENT = "Message sent to {}: {}"
    MESSAGE_SENDING_ERROR = "Error while sending message: {}"
    MESSAGE_SENDING_ERROR_DEBUG = (
        "Error while sending message: {message} on channel: {channel}, error: {error}"
    )
    MESSAGE_SEND_FAILED = "Failed to send message: {}"
    MESSAGE_PROCESSING_ERROR = "Error while processing message: {}"
    MESSAGE_PROCESSING_ERROR_DEBUG = "Error while processing message: {message} on channel: {channel}, method: {method}, properties: {properties}, error: {error}"
