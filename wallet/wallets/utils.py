import requests


def request_third_party_deposit():
    response = requests.post("http://localhost:8010/")
    data = response.json()

    if data["status"] == 200:
        return True

    return False
