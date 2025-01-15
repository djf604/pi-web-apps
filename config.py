ACCOUNT_IDS = {
    'profit': 'af0b1cee-e532-11ee-9978-fbfce8dd1127',
    'income': 'af08f31a-e532-11ee-9978-53949156d824',
    'opex': '9466c2bc-e6d1-11ee-b777-77705950a17d',
    'taxes': 'a52f3660-e6d1-11ee-904d-e337570f9779',
    'owners_pay': '0539e072-84e9-11ef-aae6-43d1ba4579f3'
}

TARGET_ALLOCATIONS = {
    'OpEx': 0.15,
    'Owner\'s Pay': 0.45,
    'Profit': 0.10,
    'Taxes': 0.30
}

TRANSACTION_FILTERS = [
    ('counterpartyName', 'Amazon'),
    ('counterpartyName', 'Mercury')
]