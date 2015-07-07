__author__ = 'alex'

from setuptools import setup
from setuptools import setup, find_packages

setup(name='cp_X',
      version='0.1',
      description='Simulated Content Pack',
      url='https://github.com/alexcpn/mypy',
      author='acp',
      author_email='alexcpn@gmail.com',
      license='',
      #packages=['kpi_testdriver', 'ltecpxx'],
      packages=find_packages(),
      zip_safe=False)
