from rest_framework import serializers, status

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("uuid", "balance", "username")
        read_only_fields = ("uuid", "balance")


class WalletDepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField()

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                detail="Please enter a number bigger than zero",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return value
