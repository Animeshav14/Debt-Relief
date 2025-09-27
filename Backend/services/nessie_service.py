import requests
from config.nessie import NessieConfig

class NessieService:
    """Handles all interactions with Capital One Nessie API"""
    
    def __init__(self):
        self.base_url = NessieConfig.BASE_URL
        self.api_key = NessieConfig.API_KEY
    
    def _make_request(self, method, endpoint, data=None):
        """Helper method for making API requests"""
        url = f"{self.base_url}{endpoint}"
        params = {'key': self.api_key}
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params)
            elif method == 'POST':
                response = requests.post(url, params=params, json=data)
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Nessie API Error: {str(e)}")
            raise Exception(f"API request failed: {str(e)}")
    
    def create_customer(self, first_name, last_name):
        """Creates a customer in Nessie API"""
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "address": {
                "street_number": "123",
                "street_name": "Main St",
                "city": "Anytown",
                "state": "VA",
                "zip": "12345"
            }
        }
        
        result = self._make_request('POST', '/customers', data)
        return result.get('objectCreated', {})
    
    def create_account(self, customer_id, account_type, balance):
        """Creates an account for a customer"""
        data = {
            "type": account_type,
            "nickname": f"{account_type} account",
            "rewards": 0,
            "balance": balance
        }
        
        endpoint = f"/customers/{customer_id}/accounts"
        result = self._make_request('POST', endpoint, data)
        return result.get('objectCreated', {})
    
    def get_account(self, account_id):
        """Gets account details"""
        endpoint = f"/accounts/{account_id}"
        return self._make_request('GET', endpoint)
    
    def make_purchase(self, account_id, amount, description):
        """Simulates a purchase/payment"""
        data = {
            "merchant_id": "placeholder_merchant",
            "medium": "balance",
            "purchase_date": "2024-01-01",
            "amount": amount,
            "description": description
        }
        
        endpoint = f"/accounts/{account_id}/purchases"
        result = self._make_request('POST', endpoint, data)
        return result.get('objectCreated', {})

# Create a singleton instance
nessie_service = NessieService()