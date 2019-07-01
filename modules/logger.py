import logging, time

logClient = False

def createlogClient(filename, mydir=""):
	global logClient
	logClient = logging.getLogger(__name__)
	logClient.setLevel(logging.INFO)

	handler = logging.FileHandler('%s%s.log'%(mydir, filename))
	handler.setLevel(logging.INFO)

	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)

	# add the handlers to the logClient

	logClient.addHandler(handler)

def log(s, level="info"):
	if not logClient:
		createlogClient(str(time.time()))

	if level == "error":
		logClient.error(s)
	elif level == "debug":
		logClient.debug(s)
	else:
		logClient.info(s)
