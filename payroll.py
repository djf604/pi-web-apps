import requests
from api_keys import READ_API_KEY
from config import USE_SSL
import config
import math
import calendar
from datetime import datetime, timedelta

from api_interactions import create_transaction, get_transactions, get_account

print(f'Value of USE_SSL: {USE_SSL}')


def make_payroll_transfer(start_date: datetime, end_date: datetime, dry_run=True):
    return_values = list()
    allocations = get_payroll(start_date, end_date, give_human_names=False)

    # Ensure total amount to transfer isn't greater than total amount in Income account
    total_transfer_amount = sum([a[1] for a in allocations])
    available_funds = get_available_funds()
    if total_transfer_amount >= available_funds:
        return ['Tried to transfer ${}, but available funds are ${}'.format(total_transfer_amount, available_funds)]

    # If funds are available, make the transfer
    for account_name, transfer_amount in allocations:
        if account_name == 'Total Revenue':
            continue
        # transfer_amount = 0.01
        idemp_key = '{}to{}-{}-{}'.format(
            start_date,
            end_date,
            account_name,
            transfer_amount
        )
        # print(account_name)
        print(idemp_key)
        ret = make_transfer(
            from_account='income',
            to_account=account_name,
            amount=transfer_amount,
            # amount=0.01,
            idemp_key=idemp_key,
            dry_run=dry_run
        )
        return_values.append(ret)
    return return_values


def make_transfer(from_account, to_account, amount, idemp_key, dry_run=False):
    if not dry_run:
        response = create_transaction(
            from_account_id=config.ACCOUNT_IDS[from_account],
            to_account_id=config.RECIPIENT_IDS[to_account],
            amount=amount,
            idempotency_key=idemp_key
        ).json()
        print(response)
        if response.get('reasonForFailure') is None:
            return 'Successfully transferred ${} from {} to {}'.format(round(amount, 2), from_account, to_account)
        else:
            return 'Error in transferring ${} from {} to {}: {}'.format(round(amount, 2), from_account, to_account, response.get('errors', {}).get('message'))
    return 'Dry run: transferred ${} from {} to {}'.format(round(amount, 2), from_account, to_account)


def format_pay_periods(n_pay_periods=1):
    pay_periods = get_n_pay_periods(
        n_pay_periods=n_pay_periods
    )

    pay_periods_config = list()
    for start_date, end_date in pay_periods:
        print(start_date)
        pay_period_allocations = get_payroll(start_date, end_date)
        pay_periods_config.append({
            'start_date': start_date,
            'end_date': end_date,
            'start_date_display': start_date.strftime('%b %-d'),
            'end_date_display': end_date.strftime('%b %-d, %Y'),
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


def filter_transactions(transactions, filters):
    filtered_transactions = list()
    for t in transactions:
        for field, val in filters:
            if val in t[field]:
                break
        else:
            filtered_transactions.append(t)
    return filtered_transactions


def get_payroll(start_date: datetime, end_date: datetime, give_human_names=True):
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
    for (machine_name, human_name), alloc in config.TARGET_ALLOCATIONS.items():
        allocation_amount = math.floor(total_income * alloc * 100) / 100.0
        allocations.append((human_name if give_human_names else machine_name, allocation_amount))
    allocations.append(('Total Revenue', round(total_income, 2)))

    return allocations

def get_available_funds():
    return get_account(account_id=config.ACCOUNT_IDS['income'])['availableBalance']
