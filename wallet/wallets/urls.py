from django.urls import path

from wallets.views import CreateDepositView, ScheduleWithdrawView, CreateWalletView, RetrieveWalletView

urlpatterns = [
    path("", CreateWalletView.as_view()),
    path("<uuid>/", RetrieveWalletView.as_view()),
    path("<uuid>/deposit", CreateDepositView.as_view()),
    path("<uuid>/withdraw", ScheduleWithdrawView.as_view()),
]
