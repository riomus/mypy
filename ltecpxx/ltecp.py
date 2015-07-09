from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *

from ltecpxx import scopeservicehelper

__author__ = 'acp'

import cherrypy
import requests
import logging
import uuid


''' Test Code to mimick a Content Pack, Interfacing with SoftVim
    and KPIStorage, running a simple numerical algorithm
    and giving out some data via REST'''

print("Running in Python 3 Style")


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
    # http://127.0.0.1:8099/getscopes?nodeid=sprintlab476vm6
    def getscopes(self, nodeid):
        self.logger.info("In call to get Scopes")
        ip = "http://%s.netact.nsn-rdnet.net:9080" % nodeid
        r = requests.get(ip + "/ScopeRegistryService/v1/scopes/")
        return r.json()

    @cherrypy.expose
    # @cherrypy.tools.json_out()
    # http://127.0.0.1:8099/startoperaion?nodeid=clab869node02&scopeid=12
    # @profile
    def startoperation(self, sourcescopeid, targetscopeid, nodeid):

        try:
            sourcednlist = scopeservicehelper.getDNFromScope(nodeid, sourcescopeid)
            targetdnlist = scopeservicehelper.getDNFromScope(nodeid, targetscopeid)

            self.logger.info("Number of DNs for the Source ScopeId %s is %s", sourcescopeid, len(sourcednlist))
            self.logger.info("Number of DNs for the Target ScopeId %s is %s", targetscopeid, len(targetdnlist))

            # Batch the kpi data
            dnsublist = sublist(sourcednlist, 10)
            self.logger.info(" DN SubList size %s", dnsublist.__len__())

            self.tasklist=[{}]
            # Send the Task to Celery Queue
            import ltecpxx.mrosimpleexecutor as r

            taskid= uuid.uuid1().int
            self.tasklist.append({taskid:[]})
            for sourcedns in dnsublist:
                result = r.doTargetprefilter.delay(sourcedns, targetdnlist)
                self.tasklist[taskid].insert(result)


        except RuntimeError as e:
            self.logger.error("Exception occurred ", e.strerror, e.errno)
            raise



    startoperation._cp_config = {'response.stream': True}


if __name__ == "__main__":
    cherrypy.config.update({'server.socket_port': 8099})
    cherrypy.quickstart(LteCPX())
