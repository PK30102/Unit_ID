import requests
import os
import time
from dotenv import load_dotenv

class UnitID:
    def __init__(self):
        load_dotenv(override=True)
        self.setData()
        self.getLogindaten()
        self.getEndpoint()
        self.getToken()
        self.getTacticalUnits()
    
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
        
    def getLogindaten(self):
        print("===> Token Request Daten:")
        print("Token URL:", self.token_endpoint)
        print("client_id:", self.client_id)
        print("username:", self.username)
        print("password:", "*" * len(self.password))

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
            self.access_token = response["access_token"]
            return self.access_token
        else:
            print("Fehler beim Abrufen des Tokens:", response)
            exit()

    def getTacticalUnits(self):
        print("\n\n>>> Taktische Einheiten <<<")

        headers = {
            "Authorization" : "Bearer " + self.access_token,
            "Content-Type": "application/json;charset=UTF-8"
        }

        tactical_units = {} # Liste der Taktischen Einheiten (ID, Name) (dict)
        tu_outfile = open("TNANDS_TU-list.csv", "w")
        tu_outfile.write("id,name")

        response = requests.get(self.conference_url+"/api/v1/tactical-units", headers=headers).json()
        response_length = len(response)

        print("\n>>> "+ str(response_length) + " Einträge <<<\n")
        #print(response)
        for ctr in range(response_length):
            #print(response[ctr])
            print(str(response[ctr]['id']) +"\t"+ response[ctr]['name'])    
            tu_outfile.write("\n"+str(response[ctr]['id']) +","+ response[ctr]['name']+",")
            tactical_units[str(response[ctr]['id'])] = response[ctr]['name']

        print(str(response[1]))
        #print(tactical_units)
        tu_outfile.close()

UnitID()