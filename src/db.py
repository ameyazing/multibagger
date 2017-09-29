from pymongo import MongoClient
import pymongo
import logging
import sys

#TODO: Replace this global variable with state maintained in Actor-model / gen_server
GLOBAL_DB = None

#If connection is already established, return connection handle
#If connection is not establish, establish a new connectin and return connection handle
def establish_conn():
	global GLOBAL_DB
	if  GLOBAL_DB != None:
		return GLOBAL_DB
	client = MongoClient()
	try:
		client.admin.command('ismaster')
	except pymongo.errors.ConnectionFailure:
		logging.error("Failed to establish connection to db")
		client = None
		return None
	GLOBAL_DB = client.stocks
	return GLOBAL_DB

def db_transact(db_func, pObj):
	try:
		obj = db_func(pObj)
	except pymongo.errors.ConnectionFailure:
		logging.error("DB Connection Failure")
	except:
		logging.error("Unhandled exception")

#criteria: JSON object which will be the criteria for which doc to update
#upsert: Create new doc if criteria fails
#obj: JSON object containing all keys who's values need to be udpated
#Return value: _id of the updated document if successful, else None
def db_modify_one(pISIN, obj, criteria, upsert=True, replace=False):
	db = establish_conn()
	if db == None:
		return None
	update_result = None
	try:
		if replace == True:
			print("Replacing ISIN: {}".format(pISIN))
			update_result = db.stocks.replace_one({"isin":pISIN},obj, upsert=upsert)
		else:
			print("Updating ISIN: {}".format(pISIN))
			update_result = db.stocks.update_one({"isin":pISIN},{"$set":obj}, upsert=upsert)
	except pymongo.errors.ConnectionFailure:
		logging.error("DB Connection Failure")
	except pymongo.errors.ConfigurationError:
		logging.error("DB Configuration Error")
	except pymongo.errors.CollectionInvalid:
		logging.error("DB Collection Invalid")
	except pymongo.errors.InvalidName:
		logging.error("DB Invalid Name")
	except pymongo.errors.InvalidOperation:
		logging.error("DB Invalid Operation")
	except pymongo.errors.InvalidURI:
		logging.error("DB Invalid URI")
	except pymongo.errors.NetworkTimeout:
		logging.error("DB Network Timeout")
#	except pymongo.errors.WriteError:
#		logging.error("DB Write Error")
	except Exception as e:
		logging.error("DB Unhandled error; {}".format(e))
	if update_result.acknowledged == True:
		return update_result.upserted_id
	else:
		logging.warning("Upsert Failed for ISIN: {}".format(pISIN))
		return None

def db_write_company(ISIN, obj, replace = False):
	logging.info("Recd ISIN: {}; obj: {}".format(ISIN, obj))
	db = establish_conn()
	if db == None:
		return None
	updated_id = db_modify_one(ISIN, obj, {"isin":ISIN}, upsert=True, replace=replace)
	if updated_id == None:
		return None

def test_function():
	stock1 = {
		'isin': '1234567890',
		'company_name': 'Maruti Suzuki India',
		'main_page_url': 'http://www.moneycontrol.com/india/stockpricequote/autocarsjeeps/marutisuzukiindia/MS24',
		'company_id': 'MU01',
		'sector_name': 'Automotive',
		'sector_id': 'AU'
	}
	db_handle = establish_conn()
	if db_handle == None:
		print("Failed to establish connection")
		return
	db_write_company("1234567890", stock1, replace=True)
	#db_write_company("1234567890", stock1, replace=False)

if __name__ == "__main__":
	print("Executing db __main__")
	test_function()
