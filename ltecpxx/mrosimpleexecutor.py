__author__ = 'alex'

from celery import Celery

app = Celery('tasks', backend='rpc://',broker='amqp://guest@10.0.3.15//')


'''
Get the targetcells from the sourcedns and if it is not present in tragetdnlist
remove those
'''
@app.task
def doTargetprefilter(sourcednlist,targetdnlist):

    #get the Kpi's for sourcednlist
    print("Source DN list length is %d" % len(sourcednlist))


class SimplePrefilter():

    def prefilterTargets(self,sourcednlist,targetdnlist):
        pass

