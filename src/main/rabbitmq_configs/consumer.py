import pika
import os
from dotenv import load_dotenv

from .callback import rabbitmq_callback

load_dotenv()


class RabbitMqConsumer:
    def __init__(self) -> None:
        self.__host = os.getenv("RABBITMQ_HOST", "localhost")
        self.__port = int(os.getenv("RABBITMQ_PORT", "5672"))
        self.__username = os.getenv("RABBITMQ_USERNAME", "guest")
        self.__password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.__queue = "default_queue"
        self.__routing_key = ""
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
        channel.queue_bind(
            exchange="default_exchange",
            queue=self.__queue,
            routing_key=self.__routing_key
        )
        channel.basic_consume(
            queue=self.__queue,
            on_message_callback=rabbitmq_callback,
            auto_ack=True
        )

        return channel

    def start_consuming(self) -> None:
        self.__channel.start_consuming()
