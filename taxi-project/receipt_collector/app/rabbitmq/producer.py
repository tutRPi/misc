import json
import os
import pika

queue_name = os.getenv("RABBITMQ_NEW_RECEIPT_ROUTING_KEY")
parameters = pika.URLParameters(os.getenv("RABBITMQ_URL"))

connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)

# TODO ensure thread safety and handle connection closures
# https://github.com/pika/pika/blob/main/examples/asynchronous_publisher_example.py


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(body), properties=properties)
