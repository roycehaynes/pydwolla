## Summary

Pydwolla is an elegant API wrapper for Dwolla. You can do tasks like register new user, add a new bank account, transfer funds and more.

## Installation

Use [pip](http://www.pip-installer.org/en/latest/) to install,

```

pip install pydwolla

```

This installs pydwolla and its dependency package, [requests](http://docs.python-requests.org/en/latest/)

Note: Pydwolla works on python v2.7.2 and greater.

## Tutorial

#### Step 0: [Sign up](http://www.dwolla.com) for Dwolla and [register a new application](https://www.dwolla.com/applications). It's free.

![Regiter Dwolla application](http://i.imgur.com/NY7ZYLD.jpg)


#### Step 1: Initialize Pydwolla with the key and secret from previous step. 


```

from pydwolla import dwolla

KEY = 'your client id here'
SECRET = 'your client secret here'

dwolla.init(KEY, SECRET)

```

To get a Dwolla user's oauth token (also known as access token), you'll need to reach out to Dwolla's website with a url. Use the dwolla.request_token_url() function to create the url:

```
url = dwolla.request_token_url(scope='AccountInfoFull')

```

When a user goes to the url and allows your app permissions to their account, a code will be sent to your callback url specified either when you created your app or passed as an argument to dwolla.request_token_url(). You'll need this code to grab the oauth token.

#### Step 2: Get user's oauth token

```
oauth_token = dwolla.get_oauth_token(code='code goes here')

```

[Learn more about Dwolla's authentication process](https://developers.dwolla.com/dev/pages/auth#oauth-token)

#### Step 3: Start using Dwolla's API. For example, get a Dwolla user's transactions.

```
transactions = dwolla.Transaction.all()

```

If successful, a dictionary will return in the following format:

```

{
    'Message': 'some message',
    'Success': true,
    'Response': [
        { "Amount" : 0.25,
        "ClearingDate" : "",
        "Date" : "02/23/1985 11:55:43",
        "DestinationId" : "888-321-4567",
        "DestinationName" : "Royce Haynes",
        "Fees" : null,
        "Id" : 14577895,
        "Notes" : "Refund for transaction ID: 14577895. Chunk 1 of 1.",
        "SourceId" : "812-987-1244",
        "SourceName" : "Reflector by Dwolla",
        "Status" : "processed",
        "Type" : "money_received",
        "UserType" : "Dwolla"
      }
    ]
}

```

#### Step 4: Take a look at the examples.


## Current Version

0.1

## Author

Pydwolla is currently developed and maintained by [Royce Haynes](http://www.roycehaynes.com) (royce.haynes@gmail.com). 

