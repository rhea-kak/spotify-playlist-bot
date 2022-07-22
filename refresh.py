from secrets import refresh_token, base_64_encoded_ids
import json
import requests


class Refresh:

    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64_encoded_ids = base_64_encoded_ids

    def refresh_auth_token(self):

        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query, data={"grant_type": "refresh_token", "refresh_token": refresh_token},
                                 headers={"Authorization": "Basic " + base_64_encoded_ids})

        response_json = response.json()

        return response_json["access_token"]
