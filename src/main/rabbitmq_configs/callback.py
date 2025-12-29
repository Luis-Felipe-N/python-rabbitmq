import json

from src.drivers import telegram_sender


def rabbitmq_callback(ch, method, properties, body):
    message = body.decode("utf-8")
    formatted_message = json.loads(message)
    print("Received message:", formatted_message)
    telegram_sender.send_telegram_message(formatted_message["message"])
