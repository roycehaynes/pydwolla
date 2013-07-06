import dwolla


KEY = 'key goes here'
SECRET = 'secret goes here'
TOKEN = 'token goes here'

# initialize dwolla
dwolla.init(KEY, SECRET, TOKEN)

"""
 Part 1: Grab stats for user associated to the TOKEN
"""
stats = dwolla.Transactions.stats()

print stats.get('Response')

# Learn more about transaction status at https://developers.dwolla.com/dev/docs/transactions/stats

"""
    Part 2: Grab all transactions for a user
"""
transactions = dwolla.Transactions.all()

print transactions.get('Response')

"""
Part 3: Grab detailed info about a transaction for a user
"""

transaction = dwolla.Transactions.retrieve(transactions.get('Response')[0]['Id']) 

print transaction.get('Response')
