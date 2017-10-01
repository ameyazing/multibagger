import logging
import time
import csv
from datetime import datetime
import os
import moneycontrol_crawler as mc

def setup_logging():
	#setup logging
	timestamp = time.time()
	ts = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d--%H-%M-%S')
	log_file_name="./log/{s_TS}.log".format(s_TS=ts)
	os.makedirs(log_file_name[:log_file_name.rindex(os.path.sep)], exist_ok=True)
	logging.basicConfig(filename=log_file_name,
						filemode='a',
						format='%(asctime)s, %(name)s %(module)s:%(lineno)d %(levelname)s %(message)s',
						datefmt='%H:%M:%S',
						level=logging.DEBUG)
	logging.info("Multibagger logger setup... Done.")
	logger_obj = logging.getLogger('multibagger')

def update_all_data(pISIN):
	success = mc.update_all_data(pISIN)
	if success == True:
		logging.info("All data successfully update")
	else:
		logging.warning("All data NOT successfully updated")

def loadFromFile(pFileName):
	try:
		fd = open(pFileName, 'r')
	except OSError(errno, strerr):
		logging.error("Unable to load ISIN.dat: {s_err}".format(s_err=strerr))
		return []
	except IOError:
		logging.error("Unable to load ISIN.dat: IOError")
		return []
	ISINs = fd.read().splitlines()
	return ISINs

if __name__ == "__main__":
	setup_logging()
	ISINs = loadFromFile("../data/ISIN.dat")
	update_all_data(ISINs)
	#download_daily_data(ISINs)
	#download_periodic_data()

