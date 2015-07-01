__author__ = 'acp'


import cherrypy
import json
import numpy



class KpiDriver(object):


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def POST(self,sourcednlist,kpinamelist,starttime,endtime):
         print("Got a post request")
         r= self.createJsonforKpiname(sourcednlist,kpinamelist)
         k= self.createmainJsonStr(r,starttime,endtime)
         return  k


    def createJsonforKpiname(self,sourcednlist,kpinamelist):
        data={'values':[]}
        for sourcedn in sourcednlist:
            kpidata={"sourceDN": sourcedn, "targetDN": sourcedn+'/target'}
            for kpi in kpinamelist:
                kpidata[kpi]=numpy.round(numpy.random.uniform(0, 100,),2)
            data['values'].append(kpidata)
        return  data

    def createmainJsonStr(self,kpinamejson,periodStart,periodEnd):
        data={"period":{"periodStart":periodStart,"periodEnd":periodEnd}}
        r=data.copy()
        r.update(kpinamejson)
        return r


