__author__ = 'acp'

import cherrypy
import requests
import logging
import time
import json

from multiprocessing import Pool


''' Test Code to mimick a Content Pack, Interfacing with SoftVim
    and KPIStorage, running a simple numerical algorithm
    and giving out some data via REST'''


def sublist(thislist, chunksize):
    mylist = []
    while len(thislist) > 0:
        a = thislist[:chunksize]
        mylist.append(a)
        del (thislist[:chunksize])

    return mylist


def sublistYeild(thislist, chunksize):
    while len(thislist) > 0:
        a = thislist[:chunksize]
        yield a
        del (thislist[:chunksize])


class LteCPX(object):
    logger = None
    ip = None

    kpiNames = ["vim.eutran.latehocount",
                "vim.eutran.earlyhocount",
                "vim.eutran.wrongcelltargethocount",
                "vim.eutran.pingpongcount",
                "vim.eutran.handoversuccess",
                "vim.eutran.wrongcellresethocount",
                "vim.eutran.handoverattempts",
                "vim.eutran.handoverfailurecount",
                "vim.eutran.handoverfailurerate",
                "vim.eutran.pingponghandoverrate"]

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        hdlr = logging.FileHandler('/tmp/myapp.log')
        # create console handler with a higher log level
        console = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        console.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.INFO)
        return

    @cherrypy.expose
    def index(self):
        return "LTE CPX - Check Manual for various Operations!"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    # http://127.0.0.1:8099/getscopes?nodeid=clab869node02
    def getscopes(self, nodeid):
        self.logger.info("In call to get Scopes")
        ip = "http://%s.netact.nsn-rdnet.net:9080" % nodeid
        r = requests.get(ip + "/ScopeRegistryService/v1/scopes/")
        return r.json()

    # To test streaming
    @cherrypy.expose
    # http://127.0.0.1:8099/stest
    def test(self):
        for i in range(0, 20):
            yield "Hello\n"
            time.sleep(1)
            yield "World -Power of yeild\n"
            # Enable streaming for the ping method.  Without this it won't work.

    test._cp_config = {'response.stream': True}

    @cherrypy.expose
    # @cherrypy.tools.json_out()
    # http://127.0.0.1:8099/startoperaion?nodeid=clab869node02&scopeid=12
    # @profile
    def startoperation(self, scopeid, nodeid):

        try:
            dnlist = []
            self.ip = "http://%s.netact.nsn-rdnet.net:9080" % nodeid
            r = requests.get(self.ip + "/ScopeRegistryService/v1/scopes/" + scopeid + "/elements/resolve")
            for key in r.json():  # iterate over a list
                dnlist.append(key['elementId'])  # get element from a dict - which has the DN

            self.logger.info("Number of DNs for the ScopeId %s is %s", scopeid, len(dnlist))
            if len(dnlist) == 0:
                return "No DNs for the Specific Scope"
            self.logger.info(" DN for scope are %s", dnlist)

            # Batch the kpi data
            dnsublist = sublist(dnlist, 10)

            self.logger.info(" DN SubList size %s", dnsublist.__len__())

            if dnsublist.__len__() > 0:
                output = map(self.getKPIs, dnsublist[:1])  # for the tiem being give only one sybset
                for e in list(output):
                    yield e
                    yield "Next Output"

            else:
                yield "No DNs to Expose"

        except RuntimeError as e:
            self.logger.error("Exception occurred ", e.strerror, e.errno)
            raise

    startoperation._cp_config = {'response.stream': True}

    def getKPIs(self, scopelist):

        '''formdata = {

            "scope": ",".join(scopelist),
            "kpi_name": ",".join(self.kpiNames),
            "kpiRetrievalFilter": "WEEK,SUM,1,true"
        }
        # //get the KPI data for the DN from Real KPIStorage - Commemeted out for time being
        requestid = requests.post(self.ip + "/KPIStorage/v1/KPIS", data=formdata)
        self.logger.info("Request ID received from KPIStorage is %s", requestid.text)
        jsonop = requestid.json()
        self.logger.info("Request URL received from KPIStorage is %s", jsonop['url'])
        kpidata = requests.get(jsonop['url'])'''

        #Use A dummy KPI Testdriver instead

        kpidata = requests.post("http://127.0.0.1:8081/kpidriver/POST",
                          data={'sourcednlist': scopelist, 'kpinamelist': self.kpiNames, 'starttime': "12-01-2015",
                                'endtime': '12-06-2015'})

        r = ""

        return r


        # go through the list
        # r = requests.get(ip + "/softvimapp/v1/CM/1/")


if __name__ == "__main__":
    cherrypy.config.update({'server.socket_port': 8099})
    cherrypy.quickstart(LteCPX())
