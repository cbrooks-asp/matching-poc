import os
import re
import pandas as pd
from thefuzz import process

# load our list of merchants
merchants_filename = "data/hip.csv"
merchants = pd.read_csv(merchants_filename)

all_merchants = [merchant for merchant in merchants["brand_name"] if not(pd.isnull(merchant))]

# load our list of transactions
transactions_filename = "data/x00"
transactions = pd.read_csv(transactions_filename, usecols=[0,1,2], names=['id1', 'id2', 'display_name'])

all_transactions = [txn for txn in transactions['display_name'] if not(pd.isnull(txn))]

iterator = 0

# Perform fuzzy string matching
for t in all_transactions:
    # strip out transaction information that might not be relevant to matching the merchant
    cleaned_txn = re.split(r'[\\\#\(\-\,]', t, 1)[0]

    normalized_merchant = process.extractOne(cleaned_txn, all_merchants)
    print(cleaned_txn, normalized_merchant, t)
    iterator += 1
    if (iterator > 100):
        break
