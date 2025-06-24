import requests
import os
import time
from dotenv import load_dotenv

class UnitID:
    def __init__(self):
        load_dotenv()
        self.setData()
        self.getEndpoint()
        self.getToken()
    
    def setData(self):
        self.token_endpoint = None
        self.conference_url = os.getenv("url")
        self.client_id = os.getenv("client_id")
        self.client_credentials = os.getenv("client_secret")
        self.username = os.getenv("username")
        self.password = os.getenv("password")
        self.tactical_unit = os.getenv("tactical_unit")
        if not all([self.client_id, self.client_credentials, self.username, self.password]):
            raise ValueError("Fehlende Umgebungsvariablen: CLIENT_ID, CLIENT_CREDENTIALS, USERNAME und PASSWORD müssen gesetzt sein.")

    def getEndpoint(self):
        try:
            response = requests.get(self.conference_url + "/api/about")
            response.raise_for_status()
            oAuthIssuerURL = response.json()['authentication']['issuer']

            response = requests.get(oAuthIssuerURL + "/.well-known/openid-configuration")
            response.raise_for_status()
            self.token_endpoint = response.json()['token_endpoint']
            print(self.token_endpoint)

            return self.token_endpoint
        except Exception as e:
            raise RuntimeError(f"Fehler beim Abrufen des Token-Endpunkts: {e}")

    def getToken(self):
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_credentials,
            "username": self.username,
            "password": self.password
        }
        response = requests.post(self.token_endpoint, data=data).json()

        if "access_token" in response:
            access_token = response["access_token"]
            return access_token
        else:
            print("Fehler beim Abrufen des Tokens:", response)
            exit()

UnitID()