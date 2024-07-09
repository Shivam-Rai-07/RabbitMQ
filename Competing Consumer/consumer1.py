# pika is the client library for rabbitMq
import pika
from callback import perform

print("\nConsuming message via Consumer 1")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)

connection = pika.BlockingConnection(connection_parameters)

# We always interact with broker using a channel
channel = connection.channel() 

channel.queue_declare(queue = 'letterbox')

# Prefetch count implies the number of messages the consumer can have at a time.
# In other words, prefetch also means that message will not be pushed to the consumer if it already has x number of messages.
# If we don't set prefetch count, the messages will be delivered in round-robin format
channel.basic_qos(prefetch_count = 1)

channel.basic_consume(queue = 'letterbox', on_message_callback = perform)

channel.start_consuming()