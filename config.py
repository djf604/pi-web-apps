ACCOUNT_IDS = {
    'profit': 'af0b1cee-e532-11ee-9978-fbfce8dd1127',
    'income': 'af08f31a-e532-11ee-9978-53949156d824',
    'opex': '9466c2bc-e6d1-11ee-b777-77705950a17d',
    'taxes': 'a52f3660-e6d1-11ee-904d-e337570f9779',
    'owners_pay': '0539e072-84e9-11ef-aae6-43d1ba4579f3'
}

RECIPIENT_IDS = {
    'profit': '14c0838e-35c4-11f0-a624-ffe03d08c3be',
    'income': '1805fa2e-35c4-11f0-8b37-df6e5d066e84',
    'opex': '1874e452-35c4-11f0-b4bc-1b662f64e442',
    'taxes': '18c09e74-35c4-11f0-8a81-73e6e15068d2',
    'owners_pay': '1962c9ec-35c4-11f0-8cf3-3b46cc2ba2b5'
}

TARGET_ALLOCATIONS = {
    # (machine_readable_name, human_readable_name): percent
    ('opex', 'OpEx'): 0.15,
    ('owners_pay', 'Owner\'s Pay'): 0.45,
    ('profit', 'Profit'): 0.10,
    ('taxes', 'Taxes'): 0.30
}

TRANSACTION_FILTERS = [
    ('counterpartyName', 'Amazon'),
    ('counterpartyName', 'Mercury'),
    ('counterpartyName', 'internal-taxes'),
    ('counterpartyName', 'internal-profit'),
    ('counterpartyName', 'internal-ownerspay'),
    ('counterpartyName', 'internal-opex'),
]

USE_SSL = True

# Local config can override any of the above
try:
    from local_config import *
except ImportError:
    pass  # No local config, so use all of the above
