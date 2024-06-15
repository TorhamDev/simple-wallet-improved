from rest_framework import serializers

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("uuid", "balance", "username")
        read_only_fields = ("uuid", "balance")
