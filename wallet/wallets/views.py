from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from wallets import serializers
from wallets.models import Wallet


class CreateWalletView(CreateAPIView):
    serializer_class = serializers.WalletSerializer


class RetrieveWalletView(RetrieveAPIView):
    serializer_class = serializers.WalletSerializer
    queryset = Wallet.objects.all()
    lookup_field = "uuid"


class CreateDepositView(APIView):
    def post(self, request, uuid, *args, **kwargs):
        wallet = get_object_or_404(Wallet, uuid=uuid)

        serializer = serializers.WalletDepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet.deposit(amount=serializer.data["amount"])

        return Response(serializer.data)


class ScheduleWithdrawView(APIView):
    def post(self, request, uuid, *args, **kwargs):
        wallet = get_object_or_404(Wallet, uuid=uuid)

        serializer = serializers.CreateTransactionSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tr = wallet.withdraw(
            amount=serializer.validated_data["amount"],
            draw_time=serializer.validated_data["draw_time"],
        )

        return Response(serializers.TransactionSerializer(instance=tr).data)
