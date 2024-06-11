# pika is the client library for rabbitMq
import pika
from pika.exchange_type import ExchangeType

print("Producing message")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)

connection = pika.BlockingConnection(connection_parameters)

# We always interact with broker using a channel
channel = connection.channel()

# We need to declare which type of exchange are we using incase exchange is not default.
channel.exchange_declare(exchange = 'fan-out', exchange_type = ExchangeType.fanout)

message = "Hello! I want to broadcast this message to all the consumers."

channel.basic_publish(exchange = 'fan-out', routing_key = '', body = message)

print(f"\nSent message: {message}")

connection.close()
