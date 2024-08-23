# pika is the client library for rabbitMq
import pika
from pika.exchange_type import ExchangeType

print("Producing message to Direct Exchange")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)

connection = pika.BlockingConnection(connection_parameters)

# We always interact with broker using a channel
channel = connection.channel()

# We need to declare which type of exchange are we using incase exchange is not default.
channel.exchange_declare(exchange = 'direct-exchange', exchange_type = ExchangeType.direct)

routing_array = ['user', 'payment', 'all']

for routing_key in routing_array:
    message = f"Hello! This is a new message with routing key as {routing_key} published to direct exchange."
    channel.basic_publish(exchange = 'direct-exchange', routing_key = routing_key, body = message)
    print(f"\nSent message: {message}")

connection.close()
