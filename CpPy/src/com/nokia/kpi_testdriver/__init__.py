import cherrypy

from CpPy.src.com.nokia.kpi_testdriver.kpidriver import KpiDriver

__author__ = 'acp'

if __name__ == "__main__":
    cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.quickstart(KpiDriver(),'/kpidriver')