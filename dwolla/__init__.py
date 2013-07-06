"""
Pydwolla is a client library for Dwolla's API version 2. By using Pydwolla, you can
do Dwolla things like register new user, add bank account, or transfer funds.

For more information, visit https://github.com/roycehaynes/pydwolla

Author: Royce, royce.haynes@gmail.com
Publish Date: 01 Jul 2013

Reference(s):

    http://developers.dwolla.com/dev/docs/auth
"""

import requests
import json
import urllib

BASE_OAUTH_URL = "https://www.dwolla.com/oauth"
BASE_REST_URL = BASE_OAUTH_URL + "/rest"
API_VERSION = "v2"
OAUTH_TOKEN = None
CLIENT_ID = None
CLIENT_SECRET = None


class DwollaError(Exception):

    def __init__(self, message=None, http_body=None, http_status=None, json_body=None):
        super(DwollaError, self).__init__(message)
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body


class APIError(DwollaError):
    pass


class APIConnectionError(DwollaError):
    pass


class AuthenticationError(DwollaError):
    pass


def init(client_id, client_secret, oauth_token=None):
    global CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN

    CLIENT_ID = client_id
    CLIENT_SECRET = client_secret
    OAUTH_TOKEN = oauth_token if not None else OAUTH_TOKEN


def request_token_url(**kwargs):
    """ Use this method to create and return a URL that sends folks to Dwolla's OAuth permissions dialog pop-up.
    """
    global CLIENT_ID, BASE_OAUTH_URL, API_VERSION
    
    data = {
        'client_id': kwargs.get('client_id', CLIENT_ID),
        'response_type': kwargs.get('response_type', 'code'),
        'scope': kwargs.get('scope','AccountInfoFull')
    }

    data.update({k:v for (k,v) in kwargs.items() if k not in data})

    request_token_url = "{0}/{1}/authenticate".format(BASE_OAUTH_URL, API_VERSION)

    return "{0}?{1}".format(request_token_url, urllib.urlencode(data))


def get_oauth_token(**kwargs):
    """ Use this method to exchange code for oauth_token
    """

    global OAUTH_TOKEN, CLIENT_ID, CLIENT_SECRET, BASE_OAUTH_URL, API_VERSION

    try:
        data = {
            'code': kwargs['code'],
            'client_id': kwargs.get('client_id', CLIENT_ID),
            'client_secret': kwargs.get('client_secret', CLIENT_SECRET),
            'grant_type': kwargs.get('grant_type', 'authorization_code')
        }
    except KeyError as e:
        APIError(message='Missing required field {0}'.format(e))

    if kwargs.get('redirect_uri', None):
        data['redirect_uri'] = redirect_uri

    oauth_token_url = "{0}/{1}/token".format(BASE_OAUTH_URL, API_VERSION)

    resp = requests.get(oauth_token_url, params=data, verify=True)

    if 'access_token' not in resp.json():
        return resp.json()    
    
    OAUTH_TOKEN = resp.json()['access_token']

    return OAUTH_TOKEN
    


class Resource(object):
    """ Dwolla Resource abstract interface
    """

    def __init__(self, **kwargs):
        self.request = Requestor()

    @classmethod
    def retrieve(cls):
        raise NotImplementedError()

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def all(cls):
        raise NotImplementedError()

    @classmethod
    def delete(cls):
        raise NotImplementedError()

    @classmethod
    def filter(cls):
        raise NotImplementedError()

class Requestor(requests.Session):
    """ Network transport
    """

    def __init__(self, *args, **kwargs):
        super(Requestor, self).__init__(*args, **kwargs)

        self.api_url = BASE_REST_URL

        self.headers = {
            'Content-Type': 'application/json'
        }

    def get(self, controller, append_slash=True, *args, **kwargs):
        url = '{0}/{1}'.format(self.api_url, controller)
        url = '{0}/'.format(url) if append_slash else url

        resp = super(Requestor, self).get(url, *args, **kwargs)

        try:
            return resp.json()
        except ValueError as e:
            return {'Success': False, 'Message': 'Something bad happened: {0}'.format(e), 'Response': str(resp.content)}

    def post(self, controller, append_slash=True, *args, **kwargs):
        url = '{0}/{1}'.format(self.api_url, controller)
        url = '{0}/'.format(url) if append_slash else url

        data = kwargs.get('data', None)

        if data:
            kwargs['data'] = json.dumps(data)

        resp = super(Requestor, self).post(url, *args, **kwargs)

        try:
            return resp.json()
        except ValueError as e:
            return {'Success': False, 'Message': 'Something bad happened: {0}'.format(e), 'Response': str(resp.content)}

class User(Resource):
    """ A Dwolla User
    """

    @classmethod
    def all(cls, **kwargs):
        """ Grabs account information
        """
        return cls().request.get(
            'users',
            params={'oauth_token': kwargs.get('oauth_token', OAUTH_TOKEN)}
        )

    @classmethod
    def retrieve(cls, account_identifier, **kwargs):
        """ Grabs basic information
        """

        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
            
        return cls().request.get(
            'users/{0}'.format(account_identifier),
            append_slash=False,
            params=params
        )

    @classmethod
    def create(cls, **kwargs):
        """ Create a new Dwolla account
        """

        try:
            data = {
                "client_id": kwargs.get('client_id', CLIENT_ID),
                "client_secret": kwargs.get('client_secret', CLIENT_SECRET),
                "pin": kwargs['pin'],
                "email": kwargs['email'],
                "password": kwargs['password'],
                "firstName": kwargs['firstName'],
                "lastName": kwargs['lastName'],
                "address": kwargs['address'],
                "city": kwargs['city'],
                "state": kwargs['state'],
                "zip": kwargs['zip'],
                "phone": kwargs['phone'],
                "dateOfBirth": kwargs['dateOfBirth'],
                "type": kwargs.get('type', 'Personal'),
                "acceptTerms": kwargs.get('acceptTerms', 'false')
            }
        except KeyError as e:
            raise APIError(message="Missing required field {0}".format(e))

        data.update({k:v for (k,v) in kwargs.items() if k not in data})

        return cls().request.post('register', data=data)

class FundingSource(Resource):
    """ Sources of funding
    """  

    @classmethod
    def create(cls, **kwargs):
        data = {}
        
        try:
            data = {
                'account_number': kwargs['account_number'],
                'routing_number': kwargs['routing_number'],
                'name': kwargs['name'],
                'account_type': kwargs['account_type'],
                'oauth_token': kwargs.get('oauth_token', OAUTH_TOKEN)
            }
        except KeyError as e:
            raise APIError(message="Missing required field {0}".format(e))
        
        return cls().request.post('fundingsources', data=data)

    @classmethod
    def all(cls, **kwargs):
        return cls().request.get(
            'fundingsources',
            params={'oauth_token': kwargs.get('oauth_token', OAUTH_TOKEN)}
        )

    @classmethod
    def retrieve(cls, funding_id, **kwargs):
        return cls().request.get(
            'fundingsources/{0}'.format(funding_id), 
            append_slash=False, 
            params={'oauth_token': kwargs.get('oauth_token', OAUTH_TOKEN)}
        )

    @classmethod
    def verify(cls, **kwargs):        

        try:
            data = {
                'oauth_token': kwargs.get('oauth_token', OAUTH_TOKEN),
                'deposit1': kwargs['deposit1'],
                'deposit2': kwargs['deposit2'],
            }

            funding_id = kwargs['funding_id']
        except KeyError as e:
            raise APIError(message="Missing required field {0}".format(e))

        return cls().request.post(
            '{0}/verify'.format(funding_id), 
            append_slash=False, 
            data=data
        )


class Transaction(Resource):
    """ 
    """

    @classmethod
    def all(cls, **kwargs):
        """ List all transactiosn for a user
        """

        params = {}
        
        if OAUTH_TOKEN:
            params['oauth_token'] = OAUTH_TOKEN
        else:
            params['client_id'] = CLIENT_ID
            params['client_secret'] = CLIENT_SECRET

        params.update({k:v for (k,v) in kwargs.items() if k not in params})

        return cls().request.get(
            'transactions',
            params=params
        )

    @classmethod
    def retrieve(cls, transaction_id, **kwargs):
        """
        """
        params = {}

        if OAUTH_TOKEN:
            params['oauth_token'] = OAUTH_TOKEN
        else:
            params['client_id'] = CLIENT_ID
            params['client_secret'] = CLIENT_SECRET

        params.update({k:v for (k,v) in kwargs.items() if k not in params})

        return cls().request.get(
            '{0}/{1}'.format('transactions', transaction_id),
            append_slash=False,
            params=params
        )

    @classmethod
    def create(cls, is_guest=False, **kwargs):
        """ Send funds to a user
        """

        controller = 'transactions/send'
        
        try:

            if is_guest:
                controller = 'transactions/guestsend'

                data = {
                    'client_id': kwargs.get('client_id', CLIENT_ID),
                    'client_secret': kwargs.get('client_secret', CLIENT_SECRET),
                    'firstName': kwargs['firstName'],
                    'lastName': kwargs['lastName'],
                    'emailAddress': kwargs['emailAddress'],
                    'routingNumber': kwargs['routingNumber'],
                    'accountNumber': kwargs['accountNumber'],
                    'accountType': kwargs['accountType'],
                    'destinationId': kwargs['destinationId'],
                    'amount': kwargs['amount']
                }

            else:

                data = {
                    'oauth_token': kwargs.get('oauth_token', OAUTH_TOKEN),
                    'pin': kwargs['pin'],
                    'destinationId': kwargs['destinationId'],
                    'amount': kwargs['amount']
                }


        except KeyError as e:
            raise APIError(message="Missing required field {0}".format(e))
        
        data.update({k:v for (k,v) in kwargs.items() if k not in data})
        
        return cls().request.post(
            controller,
            append_slash=False,
            data=data
        )

    @classmethod
    def stats(cls, **kwargs):
        params = {
            'oauth_token': kwargs.get('oauth_token', OAUTH_TOKEN)
        }

        params.update({k:v for (k,v) in kwargs.items() if k not in data})

        return cls().request.get(
            'transactions/stats',
            append_slash=False,
            params=params
        )

class Request(Resource):
    """
    """

    @classmethod
    def retrieve(cls, request_id, **kwargs):
        """
        """
        return cls().request.get(
            '{0}/{1}'.format('requests', request_id),
            append_slash=False,
            params={'oauth_token': OAUTH_TOKEN}
        )

    @classmethod
    def create(cls, **kwargs):
        
        try:
            data = {
                'oauth_token': kwargs.get('oauth_token', OAUTH_TOKEN),
                'sourceId': kwargs['sourceId'],
                'amount': kwargs['amount']
            }
        except KeyError as e:
            raise APIError(message="Missing required field {0}".format(e))

        data.update({k:v for (k,v) in kwargs.items() if k not in data})

        return cls().request.post(
            'requests',
            data=data
        )

class Balance(Resource):
    """ Represents a user's Dwolla balance.
    """

    @classmethod
    def show(cls, **kwargs):
        return cls().request.get(
            'balance',
            params={'oauth_token': kwargs.get('oauth_token', OAUTH_TOKEN)}
        )


