import requests
import json
from .exceptions import APIError


class Complete:
    def __init__(self, api_key, text, model):
        self.api_key = api_key
        self.text = text
        self.model = model
        self.session = requests.Session()

    def get_response(self):
        params = {
            'api_key': self.api_key,
            'prompt': self.text
        }
        response = self.session.get(
            f'https://api.progressiveai.org/v1/{self.model}/complete', params=params)
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            print(f"Status code: {response.status_code}")
            print(f"Response content: {response.content}")
            raise
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
            raise
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            raise
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            raise
        except requests.exceptions.RequestException as err:
            print("Something went wrong with the request:", err)
            raise
        if 'error' in data:
            raise APIError(data['error'])
        return data['response']

# Usage:
# api_key = 'your-api-key'
# model = 'your-model'
# text = 'your-text'
# complete = Complete(api_key, model)
# print(complete.get_response(text))
