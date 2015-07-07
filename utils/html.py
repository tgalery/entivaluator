import requests
import logging

logger = logging.getLogger("entivaluator")

def check_json_response(response):
	if response and response.status_code == 200:
		return response.json()
	return []

def post_request(url, payload, headers):
	try:
		response = requests.post(url, data = payload, headers = headers)
		return response
	except requests.exceptions.RequestException as ex:
		logger.warning("Failed to submit data to %s and got a : %s ", url, ex)


