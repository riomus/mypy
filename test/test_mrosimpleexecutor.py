__author__ = 'alex'

from unittest import TestCase

class TestExecutor(TestCase):

    def test_doTargetprefilter(self):
        from  ltecpxx.mrosimpleexecutor import doTargetprefilter
        s=[1,2,3]
        t=[1,2,2]
        workername="ltecpxx.mrosimpleexecutor.SimplePrefilter"
        args =[None,s,t]
        kwargs={'wokername':workername}
        doTargetprefilter(*args,**kwargs)


