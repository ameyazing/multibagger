import logging
import search_stock as ss
import db

def download_period_data_for_company(company):
	print(company['company_name'])
	return True

def download_periodic_data():
	(success_count, failure_count) = db.execute_for_each_company(moneycontrol_crawler.download_periodic_data_for_company)
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

