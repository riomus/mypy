__author__ = 'alex'

from celery import Celery
from pydoc import locate
import traceback

app = Celery('tasks', backend='rpc://',broker='amqp://guest@10.0.3.15//')


'''
Get the targetcells from the sourcedns and if it is not present in tragetdnlist
remove those
'''
@app.task(bind=True,max_retries=3, default_retry_delay=1 * 60)  # retry in 1 minutes.
def doTargetprefilter(self,*args,workername=""):

    try:
        #print(kwargs)
        #workername=kwargs['wokername']
        print("Worker Name=",workername)
        print("Worker to load is %s" % workername)
        workerclass = locate(workername)
        print("Going to process Task")
        k = workerclass.process(None,*args)
        return 717
    except Exception as exc:
        print("Exception %s" ,exec)
        traceback.print_exc()
        #self.retry(exec=exec)



@app.task(bind=True,max_retries=3, default_retry_delay=1 * 60)  # retry in 1 minutes.
def doSimpleTest(self,*args,workername ):

    try:
        print("Going to process Simple Task")
        SimplePrefilter().process(*args)

        print("Worker Name=",workername)
        workerclass = locate(workername)
        print("Going to process Task")
        k = workerclass.process(None,*args)
        return 717
        return 77;
    except Exception as exc:
        print("Exception %s" ,exec)
        traceback.print_exc()
        #self.retry(exec=exec)


class SimplePrefilter():

     def process(self,sourcednlist,targetdnlist):
        print("SourceList Size=",len(sourcednlist))
        print("TargetList Size=",len(targetdnlist))
        return 1212

