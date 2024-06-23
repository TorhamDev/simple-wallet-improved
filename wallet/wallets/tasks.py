import ast
import json
from logging import getLogger
from uuid import UUID

import pika
from django.db import transaction
from django.utils import timezone

from wallet.celery import app
from wallets.constants import TransactionsStatus, TransactionsType
from wallets.models import Transaction

logger = getLogger(__name__)


@app.task()
def transactions_producer():
    # TODO: create a connection after checking the result of the query
    credentials = pika.PlainCredentials("rabbitmq", "rabbitmq")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", credentials=credentials)
    )

    channel = connection.channel()

    channel.queue_declare(queue="hello")
    print("[xxxxxxxxxxxxxxx] START PRODUCE")
    with transaction.atomic():
        now = timezone.now()
        transactions = Transaction.objects.select_for_update().filter(
            tr_type=TransactionsType.WITHDRAW,
            status__in=(TransactionsStatus.IN_PROGRESS, TransactionsStatus.RETRY),
            draw_time__lt=now,
        )

        print(f"[xxxxxxxxxxxxxxx] PRODUCE: {transactions}")
        for tr in transactions:
            channel.basic_publish(
                exchange="",
                routing_key="hello",
                body=json.dumps(
                    str(
                        {
                            "uuid": tr.uuid.__str__(),
                            "wallet_uuid": tr.wallet.uuid.__str__(),
                            "amount": tr.amount,
                        }
                    )
                ),
            )

            tr.status = TransactionsStatus.PENDING
            tr.save(update_fields=["status"])

        print("[xxxxxxxxxxxxxxx] PRODUCE IS OVER!!!!")


@app.task()
def transactions_consumer():
    credentials = pika.PlainCredentials("rabbitmq", "rabbitmq")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue="hello")

    def callback(ch, method, properties, body):
        print(f" [x] Received {json.loads(body)}")
        tr_data = ast.literal_eval(json.loads(body))
        with transaction.atomic():
            tr = (
                Transaction.objects.select_for_update()
                .filter(uuid=UUID(tr_data["uuid"]))
                .get()
            )

            withdrae = tr.wallet.withdraw(tr=tr)

            if withdrae:
                tr.status = TransactionsStatus.SUCCESS
                tr.save(update_fields=["status"])

    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
