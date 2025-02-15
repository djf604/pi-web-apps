import requests
from api_keys import READ_API_KEY
from config import USE_SSL
import config
import math
import calendar
from datetime import datetime, timedelta

print(f'Value of USE_SSL: {USE_SSL}')


def format_pay_periods(n_pay_periods=1):
    pay_periods = get_n_pay_periods(
        n_pay_periods=n_pay_periods   
    )

    pay_periods_config = list()
    for start_date, end_date in pay_periods:
        print(start_date)
        pay_period_allocations = get_payroll(start_date, end_date)
        pay_periods_config.append({
            'start_date': start_date.strftime('%b %-d'),
            'end_date': end_date.strftime('%b %-d, %Y'),
            'allocations': pay_period_allocations
        })
    return pay_periods_config



def get_n_pay_periods(n_pay_periods=1, date_format_str=None, end_date_format_str=None):
    if n_pay_periods < 1:
        raise ValueError('Must request at least 1 pay period')
    
    pay_periods = list()

    # Get the current pay period
    today = datetime.now().date()
    print('Today is: {}'.format(today))
    if today.day <= 15:
        start_date = today.replace(day=1)
        end_date = today.replace(day=15)
    else:
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        start_date = today.replace(day=16)
        end_date = today.replace(day=last_day_of_month)
    pay_periods.append((start_date, end_date))
    
    for period_i in range(1, n_pay_periods):
        if pay_periods[-1][0].day == 1:
            end_date = pay_periods[-1][0] - timedelta(days=1)
            start_date = end_date.replace(day=16)
        else:
            start_date = pay_periods[-1][0].replace(day=1)
            end_date = pay_periods[-1][0].replace(day=15)
        pay_periods.append((start_date, end_date))
    
    if date_format_str is None and end_date_format_str is None:
        return pay_periods
    
    return [(s.strftime(date_format_str), e.strftime(end_date_format_str or date_format_str)) for s, e in pay_periods]



def get_accounts():
    url = "https://api.mercury.com/api/v1/accounts"

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


def filter_transactions(transactions, filters):
    filtered_transactions = list()
    for t in transactions:
        for field, val in filters:
            if val in t[field]:
                break
        else:
            filtered_transactions.append(t)
    return filtered_transactions


def get_payroll(start_date: datetime, end_date: datetime):
    """
    start_date and end_date is inclusive
    """
    transactions = get_transactions(
        account_id=config.ACCOUNT_IDS['income'],
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d')
    )

    transactions = filter_transactions(
        transactions=transactions['transactions'],
        filters=config.TRANSACTION_FILTERS
    )

    total_income = sum([t['amount'] for t in transactions])
    # TODO Confirm that at least the amount from total_income exists in bank account
    allocations = list()
    for name, alloc in config.TARGET_ALLOCATIONS.items():
        allocation_amount = math.floor(total_income * alloc * 100) / 100.0
        allocations.append((name, allocation_amount))
    allocations.append(('Total Revenue', round(total_income, 2)))

    return allocations


def get_payroll_old(start_date:str, end_date:str):
    """
    start_date and end_date is inclusive
    """
    transactions = get_transactions(
        account_id=config.ACCOUNT_IDS['income'],
        start_date=start_date,
        end_date=end_date
    )

    transactions = filter_transactions(
        transactions=transactions['transactions'],
        filters=config.TRANSACTION_FILTERS
    )

    total_income = sum([t['amount'] for t in transactions])
    allocations = list()
    for name, alloc in config.TARGET_ALLOCATIONS.items():
        allocation_amount = math.floor(total_income * alloc * 100) / 100.0
        allocations.append((name, allocation_amount))
    allocations.append(('Total Revenue', round(total_income, 2)))

    return allocations
