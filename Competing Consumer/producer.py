# pika is the client library for rabbitMq
import pika
import time 
import random

print("Producing message")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)

connection = pika.BlockingConnection(connection_parameters)

# We always interact with broker using a channel
channel = connection.channel()

# Queue can be declared in both producer and consumer. It's an idempotent operation. 
channel.queue_declare(queue = 'letterbox')

messageId = 1

# We have used default exchange here.
while(True):
    message = f"This is message {messageId}"
    channel.basic_publish(exchange = '', routing_key = 'letterbox', body = (message))

    print(f"\nSent message: {message}")

    time.sleep(random.randint(1, 4))

    messageId += 1

connection.close()

# A producer is producing messages to an exchange which is routing message to a queue, with multiple consumers bound to that queue.
# Consumers receive message in a round-robin or on the basic of current load format.
