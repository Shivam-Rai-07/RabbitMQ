# pika is the client library for rabbitMq
import pika
from callback import perform

print("\nConsuming message")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)

connection = pika.BlockingConnection(connection_parameters)

# We always interact with broker using a channel
channel = connection.channel() 

channel.queue_declare(queue = 'letterbox')

channel.basic_consume(queue = 'letterbox', auto_ack = True, on_message_callback = perform)

channel.start_consuming()