from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *

from ltecpxx import scopeservicehelper

__author__ = 'acp'

import cherrypy
import requests
import logging
import uuid
import json
from enum import Enum
from  datetime import datetime, timedelta
from celery.result import ResultSet
from celery import Celery

''' Test Code to mimick a Content Pack, Interfacing with SoftVim
    and KPIStorage, running a simple numerical algorithm
    and giving out some data via REST'''

print("Running in Python 3 Style")

RunState = Enum('RunState', 'Submitted Started Failed Success')


def sublist(thislist,
            chunksize):
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
        self.tasklist = []
        self.completedtasklist = []
        self.failedtasklist = []
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
    def startoperation(self, sourcescopeid, targetscopeid, nodeid, batchsize=1000):

        try:
            sourcednlist = scopeservicehelper.getDNFromScope(nodeid, sourcescopeid)
            targetdnlist = scopeservicehelper.getDNFromScope(nodeid, targetscopeid)

            self.logger.info("Number of DNs for the Source ScopeId %s is %s", sourcescopeid, len(sourcednlist))
            self.logger.info("Number of DNs for the Target ScopeId %s is %s", targetscopeid, len(targetdnlist))

            # Quite simple batching solution- batch per scope and send
            dnsublist = sublist(sourcednlist, batchsize)
            self.logger.info(" DN SubList size %s", dnsublist.__len__())

            # Send to the distributed Queue
            resp = self.distributetasks(dnsublist, targetdnlist, workername="ltecpxx.mrosimpleexecutor.SimplePrefilter")

            # resp="{{TaskId: {0}, NumberofSubtasks:{1},RunState:Started }}".format(taskid,dnsublist.__len__())
            print(resp)
            return json.dumps(resp)


        except RuntimeError as e:
            self.logger.error("Exception occurred ", e.strerror, e.errno)
            raise

    def distributetasks(self, dnsublist, targetdnlist, workername=""):
        # Send the Task to Celery Queue
        import ltecpxx.mrosimpleexecutor as r

        taskid = uuid.uuid1().int  # create a unique main task id
        self.tasklist.append({taskid: ''})
        resultset = ResultSet([])
        for sourcedns in dnsublist:
            # send sub tasks for the main task to Celery
            args = (sourcedns, targetdnlist)
            kwargs= {'workername':workername}
            celery = Celery()
            celery.conf.CELERY_ALWAYS_EAGER = True
            celery.conf.CELERY_ALWAYS_EAGER = True
            result = r.doTargetprefilter.apply_async(args,kwargs)
            resultset.add(result)
            #print("Result Is Done %s Value is %d Is Done  Now %s" % (result.ready(),result.get(),result.ready()))
            print("Result Is Done %s "  % result.ready())
        self.tasklist[-1][taskid] = resultset
        print("Task List Conents", self.tasklist)
        # return the status of of the operation
        resp = {'TaskId': taskid, 'NumberofSubtasks': dnsublist.__len__(), 'RunState': str(RunState.Submitted)}
        return resp

    startoperation._cp_config = {'response.stream': True}

    '''
    Let's create a periodic thread that checks the task status
    '''

    def checkTaskStatus(self):

        for element in self.tasklist:
            print(element)
            for key in element.keys():
                resultset = element[key]
                print("TaskId=%d Sublist Count=%d" % (key, len(resultset.results)))
                subtasklist = resultset.results

                # If all tasks are succeded
                if resultset.ready() and resultset.successful():
                    self.completedtasklist.append(element)
                    self.tasklist.remove(element)
                # If at least one task is failed
                if resultset.ready() and resultset.failed():
                    self.failedtasklist.append(element)
                    self.tasklist.remove(element)


if __name__ == "__main__":
    cherrypy.config.update({'server.socket_port': 8099})
    cherrypy.quickstart(LteCPX())
