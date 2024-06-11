# pika is the client library for rabbitMQ
import pika
from pika.exchange_type import ExchangeType

def perform(channel, method, properties, body):
    print(f"\nReceived message: {body}. Consumed using consumer 1")

print("\nConsuming message via Consumer 1")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)

connection = pika.BlockingConnection(connection_parameters)

# We always interact with broker using a channel
channel = connection.channel() 

# Declaring exchange is also an idempotent operation.
channel.exchange_declare(exchange = 'fan-out', exchange_type = ExchangeType.fanout)

# Empty queue name implies that server will assign a queue name
# Exclusive = true means that queue will be automatically deleted once consumer goes down.
queue = channel.queue_declare(queue = '', exclusive = True) 

# We have to bind our queue to the exchange
# Note: In fanout exchange we don't need to specify binding_key/routing_key while binding queue to the exchange.
# In fanout exchange each queue is bound to the exchange with the binding key equal to queue name.
channel.queue_bind(exchange = 'fan-out', queue = queue.method.queue)

# Prefetch count implies the number of messages the consumer can have at a time.
channel.basic_qos(prefetch_count = 1)

channel.basic_consume(queue = queue.method.queue, auto_ack = True, on_message_callback = perform)

print(f"Queue for consumer 1 --> {queue.method.queue}")

channel.start_consuming()


# Having the consumer down and not having the queue at all are 2 different things.
# If the consumer is down, the message will get stuck in queue. As soon as the consumer comes online, the message will be delivered to the consumer.
# If the queue is not present to which the exchange is trying to route the message to, in that case the message will be lost. 