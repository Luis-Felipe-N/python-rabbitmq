import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()


def callback(ch, method, properties, body):
    message = body.decode("utf-8")
    formatted_message = json.loads(message)
    print(f"Received message: {formatted_message}")


class RabbitMqConsumer:
    def __init__(self) -> None:
        self.__host = os.getenv("RABBITMQ_HOST", "localhost")
        self.__port = int(os.getenv("RABBITMQ_PORT", "5672"))
        self.__username = os.getenv("RABBITMQ_USERNAME", "guest")
        self.__password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.__queue = "default_queue"
        self.__routing_key = "default_routing_key"
        self.__channel = self.create_channel()

    def create_channel(self):
        parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(parameters).channel()
        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )
        channel.basic_consume(
            queue=self.__queue,
            on_message_callback=callback,
            auto_ack=True
        )

        return channel

    def start_consuming(self) -> None:
        self.__channel.start_consuming()
