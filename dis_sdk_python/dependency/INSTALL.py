#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
def install_setuptools_pip(python_version):
    try:
        PATH = os.path.split(os.path.abspath(__file__))[0]
        setuptoolsPath=os.path.join(PATH,'setuptools-40.6.3')
        os.chdir(setuptoolsPath)
        os.system("{} setup.py install".format(python_version))
        pipPath=os.path.join(PATH,'pip-18.1')
        os.chdir(pipPath)
        os.system("{} setup.py install".format(python_version))
    except Exception as ex:
        print(str(ex))

