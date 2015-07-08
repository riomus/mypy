from unittest import TestCase
from multiprocessing import Pool
import time
import json
import ltecpxx.ltecp
import resource

__author__ = 'acp'


class TestLteCPX(TestCase):
    def f(self, x):
        time.sleep(1)
        return (x * x)

    def myyield(self, x):
        for i in range(1, 9):
            yield i * x

    def domap(self, x):
        return x.upper();

    def test_domap(self):
        print(self.domap("adas"))
        # with Pool(5) as p:
        #  print(p.map(self.f, [1, 2, 3]))

    def test_getKPIs(self):
        testlist = ["qewq20", "ewqeqw21", "qewq22", "ewqeqw23", "qewq24", "ewqeqw25", "qewq26", "ewqeqw27"]
        o = map(self.domap, testlist)
        k = list(o)
        #print(k)
        assert k[0] == "QEWQ20"

    def test_mapyield(self):
        mylist = [1, 2, 3, 4]
        o = map(self.myyield, mylist)
        for e in list(o):
            k=next(e,2)
        self.assertTrue(True)



    def testsublist(self):

        print("Going to test testsublist")
        mydn= "A pretty larger DN Stirng here to test and unique {0}"
        mylist=[]
        k=15
        times=1000000
        for i in range(1,(k*times)+1):
            t= mydn.format(i)
            mylist.append(t)
        self.assertTrue(len(mylist)==k*times)
        chunkedlist=ltecpxx.ltecp.sublist(mylist,times)
        self.assertTrue(len(chunkedlist)==k)
        print("Finished testsublist chunlistsize=%d" % k)


if __name__ == "__main__":
     rsrc = resource.RLIMIT_RSS
     soft, hard = resource.getrlimit(rsrc)
     print ('Soft limit starts as  :', soft)
     print ('Hard limit starts as  :', hard)
     resource.setrlimit(rsrc, (1024, 1024*2*1)) #limit to one kilobyte
     soft, hard = resource.getrlimit(rsrc)
     print('Hard limit changed to :', hard)
     print('Soft limit changed to :', soft)
     test=TestLteCPX()
     test.testsublist()
