import dwolla

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

print user

# Learn more about user registration at https://developers.dwolla.com/dev/docs/register/register