import pika
from django.core.management import BaseCommand

from django.conf import settings


def callback(ch, method, properties, body):
    print(f" [x] {ch}")
    print(f" [x] {method}")
    print(f" [x] {properties}")
    print(f" [x] {body}")


class Command(BaseCommand):
    help = 'Consume messages from queue and save to database'

    def handle(self, *args, **options):

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.HOST))
        channel = connection.channel()
        channel.exchange_declare(
            exchange=settings.EXCHANGE,
            exchange_type='fanout'
        )

        result = channel.queue_declare(queue='esports_events', exclusive=True)
        queue_name = result.method.queue

        print(queue_name)

        channel.queue_bind(exchange=settings.EXCHANGE, queue=queue_name)

        print('[*] Waiting for events')

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()
