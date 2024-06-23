# simple-wallet-improved
improved version of [simple wallet]("https://google.com")

this project's idea is to develop an online wallet with two features.

1. Deposit into the wallet
2. withdrawal from wallet with time in the future

the deposit into the wallet is not a big deal, our problem starts with Withdraw.

we have to schedule a withdrawal in the future and for this withdrawal, we have to call a third-party server(assume that it's a bank API) and charge the user account on that third party and if everything goes right we update our database and user wallet. the diagram below shows a simplified version of what have i done in this repository for the withdrawal section:

![diagram](./assets/Capture.PNG)


![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![rabbitmq](https://img.shields.io/badge/rabbitmq-%23FF6600.svg?&style=for-the-badge&logo=rabbitmq&logoColor=white)

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
