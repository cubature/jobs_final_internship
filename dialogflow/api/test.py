import requests
import json
import pprint

url = 'https://dialogflow.googleapis.com/v2beta1/parent=projects/collaborateuragence'

response = requests.get(url + "/agent")
pprint.pprint(response)