import pika
import time
from pika.exchange_type import ExchangeType

print("\nStarting Server")

def client_message_callback(channel, method, properties, body):
    print(f"\nRequest Received: {body} with correlationID: {properties.correlation_id}")
    message = f"Here's your response to correlation id {properties.correlation_id}"
    time.sleep(5)
    channel.basic_publish(
        exchange = '', 
        routing_key = properties.reply_to,
        body = message
    )
    print(f"\nSent response back to client: {message}")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel() 

channel.exchange_declare(exchange = 'direct-exchange', exchange_type = ExchangeType.direct)
channel.queue_declare(queue = 'request-queue')
channel.queue_bind(exchange = 'direct-exchange', queue = 'request-queue', routing_key = 'client-request')

channel.basic_consume(queue = 'request-queue', auto_ack = True, on_message_callback = client_message_callback)
channel.start_consuming()