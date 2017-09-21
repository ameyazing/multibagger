from pymongo import MongoClient
import logging

#TODO: Replace this global variable with state maintained in Actor-model / gen_server
DB = None

#If connection is already established, return connection handle
#If connection is not establish, establish a new connectin and return connection handle
def establish_conn():
	global DB
	if  DB != None:
		return DB
	client = MongoClient()
	try:
		client.admin.command('ismaster')
	except pymongo.errors.ConnectionFailure:
		logging.error("Failed to establish connection to db")
		client = None
		return None
	DB = client.stocks
	return DB

def db_transact(db_func, pObj):
	try:
		obj = db_func(pObj)
	except pymongo.errors.ConnectionFailure:
		logging.error("DB Connection Failure")
		pass
	except:
		logging.error("Unhandled exception")
		pass

def db_write_company(ISIN, obj, replace = False):
	print(ISIN, obj)
	db = establish_conn()
	if db == None:
		return None
	stock = db_transact(db.stocks.find_one, {"isin":ISIN})
	if stock == None:
		return None
	db_transact(db.stocks.insert_one, obj)

if __name__ == "__main__":
	stock1 = {
		'company_name': 'Maruti Suzuki India',
		'main_page_url': 'http://www.moneycontrol.com/india/stockpricequote/autocarsjeeps/marutisuzukiindia/MS24',
		'company_id': 'MU01',
		'sector_name': 'Automotive',
		'sector_id': 'AU'
	}
	db = establish_conn()
	print(db)
	db.db_write_company("1234567890", stock1)

