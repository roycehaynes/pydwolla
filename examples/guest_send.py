import dwolla

KEY = 'key goes here'
SECRET = 'secret goes here'


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

print transaction


# Learn more about guest transactions at https://developers.dwolla.com/dev/docs/transactions/guestsend
