__author__ = 'acp'


import cherrypy
import json
import numpy



class KpiDriver(object):


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def POST(self,sourcedn,kpinames,starttime,endtime):
         with open("D:\_del\jsonresp.txt") as jsonfile:
           kpidata= json.load(jsonfile)
           return kpidata

    def createJsonforKpiname(self,sourcedn,kpinamelist):
        data={'values':[]}
        kpidata={"sourceDN": sourcedn, "targetDN": sourcedn+'/target'}
        for kpi in kpinamelist:
            kpidata[kpi]=11
        data['values'].append(kpidata)
        return  data

    def createmainJsonStr(self,kpinamejson,periodStart,periodEnd):
        data={"period":{"periodStart":periodStart,"periodEnd":periodEnd}}
        r=data.copy()
        r.update(kpinamejson)
        return r


