import requests
import uuid
from api_keys import READ_API_KEY, READ_WRITE_API_KEY
from config import USE_SSL

def get_accounts():
    url = "https://api.mercury.com/api/v1/accounts"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_API_KEY}"
    }

    return requests.get(url, headers=headers, verify=USE_SSL).json()

def get_account(account_id):
    url = f"https://api.mercury.com/api/v1/account/{account_id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_API_KEY}"
    }

    return requests.get(url, headers=headers, verify=USE_SSL).json()


def get_transactions(account_id, start_date:str = None, end_date:str = None):
    url = f"https://api.mercury.com/api/v1/account/{account_id}/transactions?start={start_date}&end={end_date}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_API_KEY}"
    }

    return requests.get(url, headers=headers, verify=USE_SSL).json()

def create_transaction(from_account_id, to_account_id, amount: float, idempotency_key):
    url = f"https://api.mercury.com/api/v1/account/{from_account_id}/transactions"

    payload = {
        "recipientId": to_account_id,
        "amount": amount,
        "paymentMethod": "ach",
        "idempotencyKey": idempotency_key
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {READ_WRITE_API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response


def get_recipients():
    url = "https://api.mercury.com/api/v1/recipients"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_API_KEY}"
    }

    return requests.get(url, headers=headers).json()

    print(response.json())



def create_recipient(name, account_number):
    url = "https://api.mercury.com/api/v1/recipients"

    payload = {
        "electronicRoutingInfo": {
            "accountNumber": account_number,
            "routingNumber": "091311229",
            "electronicAccountType": "businessSavings",
            "address": {
                "address1": "2650 W Montrose Ave STE 207",
                "city": "Chicago",
                "region": "IL",
                "postalCode": "60618",
                "country": "US"
            },
        },
        "emails": ["elizabeth@renewaltherapy.org"],
        "name": name,
        "paymentMethod": "electronic",
        "nickname": name
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {READ_WRITE_API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers).json()

    print('Created recipient {} with id {}'.format(name, response['id']))
    print(response)
