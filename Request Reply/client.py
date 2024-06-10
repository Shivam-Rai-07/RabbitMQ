import pika
import uuid
from pika.exchange_type import ExchangeType

print("\nStarting Client")

def message_reply_callback(channel, method, properties, body):
    print(f"\nReceived reply from server: {body}")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange = 'direct-exchange', exchange_type = ExchangeType.direct)
channel.queue_declare(queue = 'request-queue')
channel.queue_declare(queue  = 'reply-queue')
channel.queue_bind(exchange = 'direct-exchange', queue = 'request-queue', routing_key = 'client-request')

message = 'Please give a response server'

correlation_id = str(uuid.uuid4())
channel.basic_publish (
    exchange = 'direct-exchange', 
    routing_key = 'client-request', 
    properties = pika.BasicProperties(
        reply_to = 'reply-queue',
        correlation_id = correlation_id
    ),
    body = message
)

print(f"\nSent request to server with correlationId -> {correlation_id} and message -> {message}")

channel.basic_consume(queue = 'reply-queue', auto_ack = True, on_message_callback = message_reply_callback)
channel.start_consuming()

# In this case, client publishes a message to an exchange(in this case direct exchange) which is routed to request queue.
# Server consumes message from request queue and sends back a response to reply queue using default exchange.
# Client then consumes message from reply queue to complete the request-response cycle.