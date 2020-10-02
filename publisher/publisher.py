import logging
import json
import os
import sys
import time

import pika
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError

RABBIT_HOST = os.environ.get("RABBIT_CONTAINER", "localhost")
EXCHANGE = os.environ.get("EXCHANGE", "basic_exchange")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_connection(host='localhost') -> BlockingConnection:
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=host))


def create_channel(pika_connection: BlockingConnection) -> BlockingChannel:
    return pika_connection.channel()


if __name__ == '__main__':
    logger.info("Creating a connection with %s", RABBIT_HOST)
    connected = False
    tries = 1
    while not connected and tries <= 5:
        try:
            connection = create_connection(host=RABBIT_HOST)
            channel = create_channel(connection)
            connected = True
        except AMQPConnectionError:
            logger.warning("Could not connect to rabbit. Try %s of 5", tries)
            tries += 1
            time.sleep(5)
    if not connected:
        logger.error("THe publisher could failed to connect to rabbitmq")
        sys.exit(1)

    channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')
    data_dir = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ), "data")
    messages_file = os.listdir(data_dir)
    for message_file in messages_file:
        logging.info("Publishing data from message %s", message_file)
        abs_x = os.path.join(data_dir, message_file)
        with open(abs_x, "r") as message:
            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key='',
                body=json.dumps(message.read())
            )
    connection.close()
