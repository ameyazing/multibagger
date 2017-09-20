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

def download_periodic_data():
	success = mc.download_periodic_data()
	if success == True:
		logging.info("Periodic data downloaded successfully")
	else:
		pass
	return

def download_daily_data(ISINs):
	for ISIN in ISINs:
		success = mc.download_daily_data(ISIN)
		if success == True:
			logging.info("Daily data downloaded successfully")
		else:
			pass
	return

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
	print("__main__: {0}".format(ISINs))
	download_daily_data(ISINs)
	#download_periodic_data()

