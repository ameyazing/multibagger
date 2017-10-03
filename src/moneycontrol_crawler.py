import logging
import search_stock as ss
import db
import download_page as dp

def download_periodic_data_for_company(company):
	url = company['mc_url']
	respObj = dp.download_page(url)
	if respObj.status_code != 200:
		logging.warning("Failed to download URL: {}".format(url))
		return False
	resp = respObj.text

def download_periodic_data():
	ISIN_list = [{"isin":"INE242C01024"},{"isin":"INE349W01017"},{"isin":"INE871C01020"}]
	(success_count, failure_count) = db.execute_for_each_company(download_periodic_data_for_company, {"$or":ISIN_list})
	return True

def download_daily_data():
	return True

def update_basic_info(pISIN):
	stock_info = ss.get_main_url_by_ISIN(pISIN)
	if stock_info != {}:
		#Sample of the object recd from get_main_url_by_ISIN()
		#{
		#	'company_name': 'Maruti Suzuki India',
		#	'main_page_url': 'http://www.moneycontrol.com/india/stockpricequote/autocarsjeeps/marutisuzukiindia/MS24',
		#	'company_id': 'MU01',
		#	'sector_name': 'Automotive',
		#	'sector_id': 'AU'
		#}
		obj = {
				"isin": pISIN,
				"company_name": stock_info['company_name'],
				"mc_url": stock_info['main_page_url'],
				"code_mc": stock_info['company_id'],
				"sector_primary": stock_info['sector_name'],
				"code_sector_mc": stock_info['sector_id']
		},
		obj = obj[0]
		db.db_write_company(pISIN, obj, replace=False)
	return True

def update_all_data(pISIN):
	#update_basic_info(pISIN)
	download_periodic_data()
	#download_daily_data()

if __name__ == "__main__":
	download_periodic_data()

