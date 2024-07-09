# pika is the client library for rabbitMq
import pika
from callback import perform

print("\nConsuming message via Consumer 2")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)

connection = pika.BlockingConnection(connection_parameters)

# We always interact with broker using a channel
channel = connection.channel() 

channel.queue_declare(queue = 'letterbox')

# Prefetch count implies the number of messages the consumer can have at a time.
# If we don't set prefetch count, the messages will be delivered in round-robin format
channel.basic_qos(prefetch_count = 1)

channel.basic_consume(queue = 'letterbox', on_message_callback = perform)

channel.start_consuming()