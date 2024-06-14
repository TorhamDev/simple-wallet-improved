import uuid

from django.db import models

from wallets.constants import TransactionsStatus, TransactionsType


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Transaction(BaseModel):
    amount = models.BigIntegerField()
    wallet = models.ForeignKey(
        "Wallet",
        null=True,
        on_delete=models.SET_NULL,
        related_name="transactions",
    )

    tr_type = models.CharField(
        max_length=4,
        choices=TransactionsType.choices,
        help_text="transaction type",
    )
    status = models.CharField(
        max_length=4,
        choices=TransactionsStatus.choices,
        default=TransactionsStatus.IN_PROGRESS,
    )

    def __str__(self) -> str:
        return f"{self.tr_type} {self.amount} to {self.wallet.username} wallet"


class Wallet(BaseModel):
    username = models.CharField(
        max_length=40, unique=True
    )  # just for make it look real :)
    balance = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return f"Wallet of {self.username}"

    def deposit(self, amount: int):
        # todo: deposit the amount into this wallet
        pass
