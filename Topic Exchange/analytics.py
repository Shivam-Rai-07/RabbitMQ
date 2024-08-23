# pika is the client library for rabbitMq
import pika
from pika.exchange_type import ExchangeType

def perform(channel, method, properties, body):
    print(f"\nReceived message: {body}. Consumed by analytics service")

print("\nConsuming message via Analytics service")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)

connection = pika.BlockingConnection(connection_parameters)

# We always interact with broker using a channel
channel = connection.channel() 

# Declaring exchange is also an idempotent operation.
channel.exchange_declare(exchange = 'direct-exchange', exchange_type = ExchangeType.direct)
channel.exchange_declare(exchange = 'topic-exchange', exchange_type = ExchangeType.topic)

# Empty queue name implies that server will assign a queue name
# Exclusive = true means that queue will be automatically deleted once consumer goes down.
queue = channel.queue_declare(queue = 'analytics-queue', exclusive = True) 

# Previously we were binding the queue to an exchange without any routing key. But for direct exchange we need routing key.
channel.queue_bind(exchange = 'direct-exchange', queue = 'analytics-queue', routing_key = 'all')
channel.queue_bind(exchange = 'topic-exchange', queue = 'analytics-queue', routing_key = '#.analytics')

channel.basic_qos(prefetch_count = 1)

channel.basic_consume(queue = 'analytics-queue', auto_ack = True, on_message_callback = perform)

channel.start_consuming()

# A queue can be bound with the a single exchange using multiple routing keys.
# Also a queue can be bound with multiple exchanges.

# Wildcard for single word -> *
# Wildcard for multiple words -> #