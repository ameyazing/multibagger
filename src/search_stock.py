import json
import logging
import download_page as dp

GLOBAL_URL='http://www.moneycontrol.com/mccode/common/autosuggesion.php?query={s_ISIN}&type=1&format=json&callback=suggest1'

def search_by_ISIN(pURL):
	logging.info("URL={s_URL}".format(s_URL=pURL))
	response = dp.download_page(pURL)
	return response

def parse_response(response_str, ISIN):
	start_index = response_str.find('[')
	end_index = response_str.rfind(']')
	json_str = response_str[start_index:end_index+1]
	parsed = json.loads(json_str)
	if len(parsed) > 0:
		stock_obj = parsed[0]
		if stock_obj['link_src'] == 'javascript:void(0)':
			logging.info("No company found for with ISIN {s_ISIN}".format(s_ISIN=ISIN))
			return {}
		else:
			ret_val = {
				"main_page_url" : stock_obj['link_src'],
				"sector_name" : stock_obj['sc_sector'],
				"sector_id" : stock_obj['sc_sector_id'],
				"company_name" : stock_obj['stock_name'],
				"company_id" : stock_obj['sc_id'],
			}
			return ret_val
	else:
		return {}

def get_main_url_by_ISIN(ISIN):
	resp = search_by_ISIN(GLOBAL_URL.format(s_ISIN=ISIN))
	if resp.status_code == 200:
		ret_val = parse_response(resp.text, ISIN)
		return ret_val
	else:
		logging.warning("Searching by ISIN: {s_ISIN}. Response code: {s_ERR}".format(s_ISIN=ISIN, s_ERR=str(resp.status_code)))
		return {}

if __name__ == "__main__":
	ret = get_main_url_by_ISIN('INE585B01010')
	print(ret)

#INE002A01018 -> Reliance Industries
#INE877I01016 -> Archidply
#INE585B01010 -> Maruti Suzuki
#INE600A01035 -> NOT FOUND

