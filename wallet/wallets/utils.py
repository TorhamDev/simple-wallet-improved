import requests


def request_third_party_deposit():
    response = requests.post("http://localhost:8010/")
    return response.json()
