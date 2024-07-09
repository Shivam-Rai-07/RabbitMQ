import time
import random

def perform(channel, method, properties, body):
    processing_time = random.randint(1, 6)
    print(f"\nReceived message: {body}. Will take {processing_time} seconds")
    time.sleep(processing_time)
    channel.basic_ack(delivery_tag = method.delivery_tag)
    print("Finished processing message")