import http.client, urllib.parse, configparser
import time, datetime, random
import logging

#First parameter
a = ['0', '1']

minWait = 22200 #6h10m
maxWait = 27000 #7h30m

#Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatted_date = datetime.datetime.now().strftime('%m_%d_%Y')
handler = logging.FileHandler("logs/luna-" + formatted_date + ".log")
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info("Logger initialized")

random.seed()
logger.info("Seed set")

#Second parameter
logger.info('Reading config file')
config = configparser.ConfigParser()
config.read('lunaconfig.ini')
logger.info("Done reading config file")

if('INFO' in config):
	username = config['INFO']['username']
else:
	print("ERROR: No username specified in config");
	exit(1)
	
logger.debug("Username = " + username)

while True:
	for x in a:
		logger.info("Voting for site " + x)
		body = "a=" + x + "&username=" + username

		headers = {"Content-type": "application/x-www-form-urlencoded"}
		logger.info("Creating connection")
		conn = http.client.HTTPConnection("luna.ereve.net");
		logger.info("POSTing to site")
		logger.debug(body)
		conn.request("POST", "/functions.php", body, headers)
		res = conn.getresponse();
		data = res.read();
		logger.debug("%s - %s", res.status, res.reason)
		logger.debug(data)
		conn.close()
		randsleep = random.randint(30, 120)
		logger.info("Waiting for " + str(randsleep) + " seconds before voting on next site.")
		time.sleep(randsleep)
	randint = random.randint(minWait, maxWait)
	waketime =  (datetime.datetime.now() + datetime.timedelta(0, randint)).strftime('%I:%M:%S%p')
	logger.info("Sleeping")
	logger.debug("Waiting until " + waketime + " (" + str(randint) + " seconds) before voting again.")
	time.sleep(randint)
