import unittest
import os
import sys
from urlparse import urlparse

try:
    from config import *
except ImportError:
    message = "To run tests, create config.py file inside test folder and define following test variables: \n\n"
    message += "                 CLIENT_ID \n \
                CLIENT_SECRET \n \
                OAUTH_TOKEN \n \
                CODE \n \
                ACCOUNT_IDENTIFIER \n \
                ACCOUNT_NUMBER \n \
                ACCOUNT_TYPE \n \
                ROUTING_NUMBER \n \
                PIN"
    raise Exception(message)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import dwolla



class DwollaTest(unittest.TestCase):

    def setUp(self):
        #: First thing first, initialize app credentials
        #: Note: OAUTH_TOKEN is optional
        dwolla.init(CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN)

    def test_request_token_url(self):
        """ Verifies pydwolla can create a request token url
        """

        url = urlparse(dwolla.request_token_url(scope='AccountInfoFull'))
        self.assertTrue('scope' in url.query)

    @unittest.skip('Requires dummy test data')
    def test_get_oauth_token(self):
        """ Verifies pydwolla can get oauth token
        """
        oauth_token = dwolla.get_oauth_token(
            code=CODE
        )

        self.assertTrue(dwolla.OAUTH_TOKEN is not None)

    @unittest.skip('Requires dummy test data')
    def test_register_user_success(self):
        """ Verifies pydwolla can register user successfully
        """
        resp = dwolla.User.create(**DUMMY_USER)

        self.assertTrue(resp.get('Success') == True)

    def test_retrieve_basic_acct_info(self):
        """ Verifies pydwolla can grab basic account info
        """
        
        resp = dwolla.User.retrieve(account_identifier=ACCOUNT_IDENTIFIER)
        self.assertTrue( resp.get('Success') == True )

    
    def test_retrieve_acct_info(self):
        """ Verifies pydwolla can grab account info
        """
        resp = dwolla.User.all()
        self.assertTrue( resp.get('Success') == True )


    @unittest.skip('Requires dummy test data')
    def test_create_funding_resource(self):
        """ Verifies pydwolla creates new funding source
        """
        
        resp = dwolla.FundingSource.create(
            account_number=ACCOUNT_NUMBER,
            routing_number=ROUTING_NUMBER,
            account_type=ACCOUNT_TYPE,
            name="test"
        )

        self.assertTrue(resp.get('Success') == True)

    def test_funding_sources(self):
        """ Verify pydwolla grabs all funding sources
        """

        resp = dwolla.FundingSource.all()
        self.assertTrue(resp.get('Success') == True)

    def test_retrieve_funding_source(self):
        """ Verify pydwolla can get a funding source
        """

        resp = dwolla.FundingSource.retrieve('5bca2927481c04e2e4d9917edd18de43')

        self.assertTrue(resp.get('Success') == True)

    @unittest.skip('')
    def test_create_transaction(self):
        """ Verifies pydwolla can send a transaction
        """
        
        resp = dwolla.Transaction.create(
            pin=PIN,
            destinationId='reflector@dwolla.com',
            amount='50'
        )

        self.assertTrue(resp.get('Success') == True)

    def test_retrieve_transaction_by_id(self):
        """ Verifies pydwolla retrieves transactions by id
        """
        
        resp = dwolla.Transaction.retrieve(TRANSACTION_ID)

        self.assertTrue(resp.get('Success') == True)

    def test_retrieve_transactions(self):
        """ Verifies pydwolla retrieves all transactions
        """
        resp = dwolla.Transaction.all()

        self.assertTrue(resp.get('Success') == True)


if __name__ == '__main__':
    unittest.main()
