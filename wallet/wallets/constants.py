from django.db.models import TextChoices


class TransactionsType(TextChoices):
    WITHDRAW = "W", "Withdraw"
    DIPOSIT = "D", "Diposit"


class TransactionsStatus(TextChoices):
    SUCCESS = "S", "Success"
    FAILED = "F", "Failed"
    RETRY = "R", "Retry"
    PENDING = "P", "Pending"
    IN_PROGRESS = "I", "In Progress"
