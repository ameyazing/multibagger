import logging
import requests
from requests.models import Response

MODULE_URL='http://www.moneycontrol.com/mccode/common/autosuggesion.php?query=INE002A01018&type=1&format=json&callback=suggest1'

def download_page(pURL, max_retry=3, attempt=0):
	try:
		r = requests.get(pURL)
		return r
	except requests.ConnectionError:
		logging.warning("Connection Error for URL: {}".format(pURL))
		response = Response()
		response.code = "Connection Error"
		response.error_type = "Connection"
		response.status_code = 451
		response._content = b'{"error":"Connection Error"}'
		return response
	except requests.Timeout:
		if attempt < max_retry:
			download_page(pURL, max_retry, attemp + 1)
		else:
			logging.warning("Connection Timeout for URL: {}".format(pURL))
			response = Response()
			response.code = "Timeout"
			response.error_type = "Connection"
			response.status_code = 400
			response._content = b'{"error":"Timeout"}'
			return response
	except requests.TooManyRedirects:
		logging.warning("Too Many Redirects for URL: {}".format(pURL))
		response = Response()
		response.code = "Too many redirects"
		response.error_type = "Redirects"
		response.status_code = 309
		response._content = b'{"error":"Too many redirects"}'
		return response
	except requests.RequestException as e:
		logging.warning("Generic Request Exception for URL: {}".format(pURL))
		response = Response()
		response.code = "Unknown error"
		response.error_type = "Generic"
		response.status_code = 450
		response._content = b'{"error":"Unknown error"}'
		return response

if __name__ == "__main__":
	response = download_page(MODULE_URL)
	if response.status_code == 200:
		print(response.text)
	else:
		print(response.status_code)

