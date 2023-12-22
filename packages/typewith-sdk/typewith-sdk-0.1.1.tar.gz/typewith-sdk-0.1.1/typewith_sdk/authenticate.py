import requests

class Authenticate:
    def __init__(self, api_key):
        self.token = self.generate_jwt_token(api_key)
    
    def generate_jwt_token(self, api_key):

        post_response = requests.post(
            'http://localhost:8000/api/v1/auth',
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        return post_response.json()['token']