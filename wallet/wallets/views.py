from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from wallets.models import Wallet
from wallets.serializers import WalletDepositSerializer, WalletSerializer


class CreateWalletView(CreateAPIView):
    serializer_class = WalletSerializer


class RetrieveWalletView(RetrieveAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    lookup_field = "uuid"


class CreateDepositView(APIView):
    def post(self, request, uuid, *args, **kwargs):
        wallet = get_object_or_404(Wallet, uuid=uuid)

        serializer = WalletDepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet.deposit(amount=serializer.data["amount"])

        return Response(serializer.data)


class ScheduleWithdrawView(APIView):
    def post(self, request, *args, **kwargs):
        # todo: implement withdraw logic
        pass
        return Response({})
