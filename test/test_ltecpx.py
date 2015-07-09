from unittest import TestCase
import resource

from  memory_profiler import profile
import ltecpxx
from  ltecpxx.ltecp import LteCPX
import ltecpxx.scopeservicehelper as t
from celery import Celery
import unittest.mock as mock

__author__ = 'acp'


class TestLteCPX(TestCase):
    orignalfunciton = t.getDNFromScope

    def mockgetDNFromScope(self, nodeid, scopeid):
        print("In call to mocked getDNFromScope %s" % scopeid)
        return ['a', 'b', 'c']


    def test_startoperatio(self):
        try:
            t.getDNFromScope = self.mockgetDNFromScope  # mocking call to scope service
            mytest = LteCPX()
            Celery.CELERY_ALWAYS_EAGER=True
            mytest.startoperation('sourcescopeid', 'targetscopeid', 'nodeid')
        finally:
            t.getDNFromScope = TestLteCPX.orignalfunciton  # reverting mock

    @profile
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
        chunkedlist = ltecpxx.ltecp.sublist(mylist, times)
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
    test.testsublist()
