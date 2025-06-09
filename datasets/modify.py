import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

num_customers = 50
num_accounts = 100
num_records = 1000

customers = [f"CUST{str(i).zfill(3)}" for i in range(1, num_customers+1)]
accounts = [f"ACC{str(i).zfill(4)}" for i in range(1001, 1001+num_accounts)]
account_customer_map = {acc: random.choice(customers) for acc in accounts}
transaction_types = ['transfer', 'payment', 'deposit', 'withdrawal']

records = []
start_time = datetime(2025, 6, 1, 9, 0, 0)

account_last_activity = {acc: None for acc in accounts}

for i in range(num_records - 100):
    sender = random.choice(accounts)
    receiver = random.choice([acc for acc in accounts if acc != sender])
    amount = round(random.uniform(100, 90000), 2)
    t_type = random.choice(transaction_types)
    timestamp = start_time + timedelta(seconds=random.randint(0, 7*24*3600))
    account_last_activity[sender] = timestamp
    account_last_activity[receiver] = timestamp
    records.append([
        i+1, timestamp.strftime('%Y-%m-%dT%H:%M:%S'), amount, 'INR',
        sender, receiver,
        account_customer_map[sender], account_customer_map[receiver],
        t_type
    ])

circle_accounts = random.sample(accounts, 3)
circle_time = start_time + timedelta(days=1, hours=2)
for j in range(3):
    sender = circle_accounts[j]
    receiver = circle_accounts[(j+1)%3]
    records.append([
        len(records)+1,
        (circle_time + timedelta(minutes=j*15)).strftime('%Y-%m-%dT%H:%M:%S'),
        120000, 'INR',
        sender, receiver,
        account_customer_map[sender], account_customer_map[receiver],
        'transfer'
    ])

sender = random.choice(accounts)
receiver_list = random.sample([acc for acc in accounts if acc != sender], 5)
rapid_time = start_time + timedelta(days=2, hours=4)
for k in range(5):
    records.append([
        len(records)+1,
        (rapid_time + timedelta(minutes=k*2)).strftime('%Y-%m-%dT%H:%M:%S'),
        round(random.uniform(140000, 180000), 2), 'INR',
        sender, receiver_list[k],
        account_customer_map[sender], account_customer_map[receiver_list[k]],
        'transfer'
    ])

acc1, acc2 = random.sample(accounts, 2)
backforth_time = start_time + timedelta(days=3, hours=5)
for m in range(6):
    s, r = (acc1, acc2) if m % 2 == 0 else (acc2, acc1)
    records.append([
        len(records)+1,
        (backforth_time + timedelta(minutes=m*3)).strftime('%Y-%m-%dT%H:%M:%S'),
        80000, 'INR',
        s, r,
        account_customer_map[s], account_customer_map[r],
        'transfer'
    ])

dormant_acc = random.choice(accounts)
spike_time = start_time + timedelta(days=6, hours=9)
for n in range(4):
    receiver = random.choice([acc for acc in accounts if acc != dormant_acc])
    records.append([
        len(records)+1,
        (spike_time + timedelta(minutes=n*4)).strftime('%Y-%m-%dT%H:%M:%S'),
        round(random.uniform(70000, 110000), 2), 'INR',
        dormant_acc, receiver,
        account_customer_map[dormant_acc], account_customer_map[receiver],
        'transfer'
    ])

for _ in range(5):
    acc = random.choice(accounts)
    fraud_type = random.choice(['deposit', 'withdrawal'])
    records.append([
        len(records)+1,
        (start_time + timedelta(days=random.randint(2, 5), minutes=random.randint(0, 300))).strftime('%Y-%m-%dT%H:%M:%S'),
        round(random.uniform(100000, 200000), 2), 'INR',
        acc, acc,  # self
        account_customer_map[acc], account_customer_map[acc],
        fraud_type
    ])

account_country_map = {acc: 'India' for acc in accounts}
foreign_accounts = random.sample(accounts, 5)
for acc in foreign_accounts:
    account_country_map[acc] = random.choice(['Russia', 'China', 'Nigeria'])
for acc in foreign_accounts:
    sender = acc
    receiver = random.choice([a for a in accounts if account_country_map[a] == 'India'])
    records.append([
        len(records)+1,
        (start_time + timedelta(days=4, hours=random.randint(0, 3))).strftime('%Y-%m-%dT%H:%M:%S'),
        130000, 'INR',
        sender, receiver,
        account_customer_map[sender], account_customer_map[receiver],
        'transfer'
    ])

cluster_accounts = random.sample(accounts, 4)
cluster_time = start_time + timedelta(days=5, hours=1)
for i in range(6):
    s, r = random.sample(cluster_accounts, 2)
    records.append([
        len(records)+1,
        (cluster_time + timedelta(minutes=i*10)).strftime('%Y-%m-%dT%H:%M:%S'),
        round(random.uniform(60000, 100000), 2), 'INR',
        s, r,
        account_customer_map[s], account_customer_map[r],
        'transfer'
    ])

columns = [
    'transaction_id', 'timestamp', 'amount', 'currency',
    'sender_account_id', 'receiver_account_id',
    'sender_customer_id', 'receiver_customer_id',
    'transaction_type'
]
df = pd.DataFrame(records, columns=columns)

df['sender_country'] = df['sender_account_id'].map(account_country_map)
df['receiver_country'] = df['receiver_account_id'].map(account_country_map)

df.to_csv('synthetic_bank_transactions2.csv', index=False)
