import os
from dotenv import load_dotenv

load_dotenv()

class NessieConfig:
    API_KEY = os.getenv('NESSIE_API_KEY')
    BASE_URL = 'http://api.nessieisreal.com'
    
    ENDPOINTS = {
        'customers': '/customers',
        'accounts': '/accounts',
        'transfers': '/transfers',
        'purchases': '/purchases'
    }
    
    @classmethod
    def get_url(cls, endpoint_name):
        # Helper to build full URLs
        return f"{cls.BASE_URL}{cls.ENDPOINTS[endpoint_name]}"
    
    @classmethod
    def get_auth_params(cls):
        # Returns API key as query parameter
        return {'key': cls.API_KEY}