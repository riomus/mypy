__author__ = 'acp'
from unittest import TestCase
from CpPy.src.com.nokia.kpi_testdriver.kpidriver import KpiDriver


class TestKpiDriver(TestCase):
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

    def test_createJson(self):
        testme = KpiDriver()
        ret=testme.createJsonforKpiname("PLMN-Slab464/MRBTS-1667/LNBTS-1667/LNCEL-5",self.kpiNames )
        print(ret)
        ret2= testme.createmainJsonStr(ret,"2015-06-08T00:00:00.000+0300","2015-06-15T00:00:00.000+0300")
        print(ret2)
