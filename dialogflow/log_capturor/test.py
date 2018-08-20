import requests
import json
import pprint

url = 'https://api.dialogflow.com/v1/query?v=20170712'
token = 'd5106a7a7d2f46dd9de001c7be158290'

headers = {
	'Authorization': 'Bearer ' + token,
	'Content-Type': 'application/json'
}