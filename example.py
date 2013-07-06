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

"""
Part 4: Create and send guest transaction
"""

DUMMY_GUEST = dict(
    client_id=KEY,
    client_secret=SECRET,
    firstName='Paul',
    lastName='Revere',
    emailAddress='samual.adams@gmail.com',
    routingNumber='11111111',
    accountNumber='17341818',
    accountType='Savings',
    destinationId='royce.haynes@gmail.com',
    amount='100000000'
)

transaction = dwolla.Transaction.create(is_guest=True, DUMMY_GUEST)

print transaction.get('Response')


# Learn more about guest transactions at https://developers.dwolla.com/dev/docs/transactions/guestsend

"""
Part 5: Register a user
"""

KEY = 'key goes here'
SECRET = 'secret goes here'

user = dwolla.User.create(
    client_id=KEY,
    client_secret=SECRET,
    pin='1234',
    email='paul.revere@gmail.com',
    password='12345678',
    firstName='Paul',
    lastName='Revere',
    address='1335 Broadway',
    city='Boulder',
    state='CO',
    zip='80211',
    phone='7134032345',
    dateOfBirth='12-21-1734',
    acceptTerms=True
)

print user.get('Response')

# Learn more about user registration at https://developers.dwolla.com/dev/docs/register/register


