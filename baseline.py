import os
import re
import json
import pandas as pd

# load our list of merchants
merchants_filename = "data/company_identification_rule.csv"
merchants = pd.read_csv(merchants_filename)

all_merchants = []
for merchant in merchants['definition']:
    # load json
    m = json.loads(merchant)
    m['re'] = re.compile(m['pattern'], re.IGNORECASE)
    all_merchants.append(m)


# load our list of transactions
transactions_filename = "data/x00"
transactions = pd.read_csv(transactions_filename, usecols=[0,1,2], names=['id1', 'id2', 'display_name'])

all_transactions = [txn for txn in transactions['display_name'] if not(pd.isnull(txn))]

iterator = 0
txn_cleaner = re.compile(r'[\\\#\(\-\,]')

# Perform fuzzy string matching
for t in all_transactions:
    # regex match
    merchant_found = False
    for m in all_merchants:
        if (m['re'].match(t)):
            merchant_found = True
            break

    # strip out transaction information that might not be relevant to matching the merchant
    cleaned_txn = txn_cleaner.split(t, 1)[0]

    print(cleaned_txn, m if merchant_found else 'NO MATCH', )
    iterator += 1
    if (iterator > 100):
        break
