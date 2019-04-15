#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

appName="a"


def deleteApp_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r=cli.deleteApp(appName=appName)
        print(r.statusCode)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("start deleteApp")
    deleteApp_test()

