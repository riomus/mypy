from unittest import TestCase
import resource
import json

from  memory_profiler import profile
from celery import Celery

from ltecpxx import ltecp
from  ltecpxx.ltecp import LteCPX
import ltecpxx.scopeservicehelper as t

__author__ = 'acp'

celery = Celery()

class TestLteCPX(TestCase):

    orignalfunciton = t.getDNFromScope

    def mockgetDNFromScope(self, nodeid, scopeid):
        print("In call to mocked getDNFromScope %s" % scopeid)
        return ['a', 'b', 'c']

    def test_startoperatio(self):
        try:
            t.getDNFromScope = self.mockgetDNFromScope  # mocking call to scope service
            mytest = LteCPX()
            Celery.CELERY_ALWAYS_EAGER = True
            ret = mytest.startoperation('sourcescopeid', 'targetscopeid', 'nodeid', batchsize=1)
            reto = json.loads(ret)
            self.assertTrue(reto['NumberofSubtasks'] == 3)
        finally:
            t.getDNFromScope = TestLteCPX.orignalfunciton  # reverting mock

    def test_checkTaskStatus(self):

        try:

            t.getDNFromScope = self.mockgetDNFromScope  # mocking call to scope service
            mytest = LteCPX()
            celery.conf.CELERY_ALWAYS_EAGER = True
            ret = mytest.startoperation('sourcescopeid', 'targetscopeid', 'nodeid', batchsize=1)
            self.assertTrue(mytest.tasklist)  # this contains one main tast
            mytest.checkTaskStatus()
            self.assertFalse(mytest.tasklist)  # this is empty of one main taks
            self.assertTrue(mytest.completedtasklist)  # this contains one main tasks
            for e in mytest.completedtasklist:
                for keys in e:
                    for r in e[keys]:
                        self.assertTrue(r.ready())  # All tasjs are done here

        finally:
            t.getDNFromScope = TestLteCPX.orignalfunciton  # reverting mock

    def test_distributetasks(self):
        mytest = LteCPX()
        sourcelist = [1, 2, 3]
        targetlist = [1, 2, 3]
        mytest.distributetasks(sourcelist, targetlist)

    # @profile
    def testsublist(self):
        print("Going to test testsublist")
        mydn = "A pretty larger DN Stirng here to test and unique {0}"
        mylist = []
        k = 15
        times = 10
        for i in range(1, (k * times) + 1):
            t = mydn.format(i)
            mylist.append(t)
        self.assertTrue(len(mylist) == k * times)
        chunkedlist = ltecp.sublist(mylist, times)
        self.assertTrue(len(chunkedlist) == k)
        print("Finished testsublist chunlistsize=%d" % k)


if __name__ == "__main__":
    rsrc = resource.RLIMIT_RSS
    soft, hard = resource.getrlimit(rsrc)
    print('Soft limit starts as  :', soft)
    print('Hard limit starts as  :', hard)
    resource.setrlimit(rsrc, (1024, 1024 * 2 * 1))  # limit to one kilobyte
    soft, hard = resource.getrlimit(rsrc)
    print('Hard limit changed to :', hard)
    print('Soft limit changed to :', soft)
    test = TestLteCPX()
    print("Going to test integration workflow")
    test.test_checkTaskStatus()
