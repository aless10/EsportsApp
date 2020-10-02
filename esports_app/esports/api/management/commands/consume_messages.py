import json
import logging
import time
from functools import wraps

import pika
from pika.exceptions import AMQPConnectionError
from django.core.management import BaseCommand

from django.conf import settings

from api.models import Event, Tournament, Team, Score, Match


logger = logging.getLogger(__name__)


def retry(exceptions, tries=3, delay=3):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            raised_exception = None
            decr_tries = tries
            while decr_tries > 0:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    raised_exception = e
                    logger.warning(f"{e}, Retrying in {delay} seconds...")
                    time.sleep(delay)
                    decr_tries -= 1
            raise raised_exception

        return wrapped

    return wrapper


def callback(ch, method, properties, body):
    logger.info('Running the callback with body %s', body)
    j_body = json.loads(body)
    data = j_body["data"]
    match_id = int(data["id"])
    state = int(data["state"])
    date_start = int(data["date_start_text"])
    Event.objects.create(  # pylint:disable=E1101
        source=j_body["source"],
        data=data
    )
    tournament = Tournament.objects.get_or_create(  # pylint:disable=E1101
        id=int(data["tournament"]["id"]),
        name=int(data["tournament"]["name"])
    )
    for team in data["teams"]:
        Team.objects.get_or_create(  # pylint:disable=E1101
            id=int(team["id"]),
            name=int(team["name"])
        )

    scores = []
    for score in data["scores"]:
        s = Score.objects.get_or_create(  # pylint:disable=E1101
            match_id=match_id,
            state=state,
            date_start=date_start,
            team=Team.objects.get(  # pylint:disable=E1101
                id=int(score["team"])
            ),
            score=score["score"],
            is_winner=score["winner"]
        )
        scores.append(s)

    Match.objects.create(  # pylint:disable=E1101
        match_id=match_id,
        state=state,
        date_start=date_start,
        tournament=tournament,
        best_of=data["best_of"],
        url=data["url"],
        title=data["title"],
        a_team_score=scores[0],
        b_team_score=scores[1],
    )


class Command(BaseCommand):
    help = 'Consume messages from queue and save to database'

    @retry((AMQPConnectionError,), tries=5, delay=3)
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

        channel.queue_bind(exchange=settings.EXCHANGE, queue=queue_name)

        logger.info('The consumer is waiting for events')

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()
