import logging
from html.parser import HTMLParser

class URLExtractor(HTMLParser):
	def handle_starttag(self, tag, attrs):
		print("Encountered a start tag: {} and attrs: {}".format(tag, attrs))

	def handle_endtag(self, tag, attrs):
		print("Encountered end tag: {} and attrs".format(tag, attrs))

	def handle_startendtag(self, tag, attrs):
		print("Encountered startend tag: {} and attrs".format(tag, attrs)

	def handle_data(self, tag, attrs):
		print("Encountered end tag: {} and attrs".format(tag, attrs))

#page: main page html.
#Sample main page URL: 'http://www.moneycontrol.com/india/stockpricequote/autocarsjeeps/marutisuzukiindia/MS24'
#Return value: JSON object with all required URLs; None if unsuccessful
def extract_main_page_urls(page):
	return None
