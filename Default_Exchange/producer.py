# pika is the client library for rabbitMq
import pika

print("Producing message")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)

connection = pika.BlockingConnection(connection_parameters)

# We always interact with broker using a channel
channel = connection.channel()

# Queue can be declared in both producer and consumer. It's an idempotent operation.
channel.queue_declare(queue = 'letterbox')

message = "Hello! Let's conquer rabbitMq"

# For default exchange, routing key should be same as the queue name
channel.basic_publish(exchange = '', routing_key = 'letterbox', body = message)

print(f"\nSent message: {message}")

connection.close()