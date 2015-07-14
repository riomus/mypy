__author__ = 'alex'

import requests
import logging

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('/tmp/myapp.log')
# create console handler with a higher log level
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
console.setFormatter(formatter)
logger.addHandler(hdlr)
logger.addHandler(console)
logger.setLevel(logging.INFO)


def getDNFromScope(nodeid, scopeid):
    dnlist = []
    ip = "http://{0}.netact.nsn-rdnet.net:9080".format(nodeid)
    requrl=ip + "/ScopeRegistryService/v1/scopes/" + scopeid + "/elements/resolve"
    logger.info("Fetching DNs from ScopeID %s" ,requrl)
    r = requests.get(requrl)

    for key in r.json():  # iterate over a list
        dnlist.append(key['elementId'])  # get element from a dict - which has the DN
    if len(dnlist) == 0:
        logger.info("No DNs for the Specific Scope")

    logger.info(" DN for scope are %d", len(dnlist))
    return dnlist
