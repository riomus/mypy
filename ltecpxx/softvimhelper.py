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


#http://10.91.113.77:9080/softvimapp/v1/CM/1/PLMN-PLMN/MRBTS-30/LNBTS-30/LNCEL-3/children?childType=LNREL&recursive=true ---------3
def getAdjacencyforSource(nodeid, sourcedn,childType='LNREL'):
    dnlist = []
    ip = "http://%s.netact.nsn-rdnet.net:9080" % nodeid
    r = requests.get(ip + "/softvimapp/v1/CM/1/" + sourcedn + "/children?childType=" +childType +"&recursive=true")