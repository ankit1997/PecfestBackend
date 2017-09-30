import json
import requests

with open('events.json', encoding='utf8') as f:
	events = json.load(f)
	headers = { 'Content-Type': 'application/json' }
	for event in events:
		print("Saving " + event['name'])
		res = requests.post('http://localhost:10001/event/create', json.dumps(event), headers=headers)
		if res.status_code is 200:
			continue
		else:
			print("Error occurred")

