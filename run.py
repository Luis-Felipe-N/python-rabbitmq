from src.main.rabbitmq_configs.consumer import RabbitMqConsumer

if __name__ == "__main__":
    rabbit_mq_consumer = RabbitMqConsumer()
    rabbit_mq_consumer.start_consuming()
