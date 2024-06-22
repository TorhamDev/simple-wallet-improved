import uuid
from datetime import datetime

from django.core.validators import MinLengthValidator
from django.db import IntegrityError, models, transaction
from django.utils import timezone

from wallets.constants import TransactionsStatus, TransactionsType
from wallets.utils import request_third_party_deposit


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

    draw_time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.tr_type} {self.amount}"  # TODO figure out deleted wallets tr to show username too


class Wallet(BaseModel):
    username = models.CharField(
        max_length=40,
        unique=True,
        blank=False,
        validators=[MinLengthValidator(limit_value=3)],
    )  # just for make it look real :)
    balance = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return f"Wallet of {self.username}"

    def get_queryset(self):
        return self.__class__.objects.filter(uuid=self.uuid)

    @transaction.atomic
    def deposit(self, *, amount: int):
        obj = self.get_queryset().select_for_update().get()
        obj.balance = models.F("balance") + amount
        obj.save()

        Transaction.objects.create(
            amount=amount,
            wallet=self,
            tr_type=TransactionsType.DIPOSIT,
            status=TransactionsStatus.SUCCESS,
        )

    @transaction.atomic
    def create_transaction_withdraw(self, *, amount: int, draw_time: datetime):
        tr = Transaction.objects.create(
            amount=amount,
            draw_time=draw_time,
            tr_type=TransactionsType.WITHDRAW,
            wallet=self,
        )

        return tr

    @transaction.atomic
    def withdraw(self, *, tr: Transaction):
        obj = self.get_queryset().select_for_update().get()
        if obj.balance > tr.amount:
            try:
                with transaction.atomic():
                    obj.balance = models.F("balance") - tr.amount
                    obj.save()

                    print("[X] Requesting to 3rd part bank!!!!!")
                    third_party = request_third_party_deposit()
                    if not third_party:
                        raise ValueError("[X] BANK ERROR")
                    return True
            except (ValueError, IntegrityError):
                tr.status = TransactionsStatus.RETRY
                tr.save(update_fields=["status"])
                return False

        print("[X] OH! wallet dosent have balance for this transaction!")
        tr.status = TransactionsStatus.FAILED
        tr.save(update_fields=["status"])

        return False
