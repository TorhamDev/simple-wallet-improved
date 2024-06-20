import json

import pika

from wallets.constants import TransactionsStatus, TransactionsType
from wallets.models import Transaction

credentials = pika.PlainCredentials("rabbitmq", "rabbitmq")
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost", credentials=credentials)
)

channel = connection.channel()

channel.queue_declare(queue="hello")

transactions = Transaction.objects.select_for_update().filter(
    tr_type=TransactionsType.WITHDRAW,
    status=TransactionsStatus.IN_PROGRESS,
)

to_update = []

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
    to_update.append(tr)


Transaction.objects.bulk_update(objs=to_update, fields=["status"])
