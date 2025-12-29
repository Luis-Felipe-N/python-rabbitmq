import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()


class RabbitMqPublisher:
    def __init__(self) -> None:
        self.__host = os.getenv("RABBITMQ_HOST", "localhost")
        self.__port = int(os.getenv("RABBITMQ_PORT", "5672"))
        self.__username = os.getenv("RABBITMQ_USERNAME", "guest")
        self.__password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.__exvhange = "default_exchange"
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
        # channel.exchange_declare(exchange=self.__exvhange, exchange_type='direct', durable=True)
        return channel

    def send_message(self, body: dict) -> None:
        self.__channel.basic_publish(
            exchange=self.__exvhange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )


rabbit_mq_publisher = RabbitMqPublisher()
rabbit_mq_publisher.send_message({"message": "Hello, RabbitMQ!"})
