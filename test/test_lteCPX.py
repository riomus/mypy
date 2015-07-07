from unittest import TestCase
from multiprocessing import Pool
import time
import json

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
        print(k)
        assert k[0] == "QEWQ20"

    def test_mapyield(self):
        mylist = [1, 2, 3, 4]
        o = map(self.myyield, mylist)
        for e in list(o):
            k=next(e,2)
        self.assertTrue(True)

    def test_parsejson(self):
        resp='{"period":{"periodStart":"2015-06-15T00:00:00.000+0300","periodEnd":"2015-06-22T00:00:00.000+0300"},"values":[]}'
        test= json.dumps(resp)
        with open("D:\_del\jsonresp.txt") as jsonfile:
            kpidata= json.load(jsonfile)

        print(kpidata['period']['periodEnd'])
        print(kpidata['values'])
