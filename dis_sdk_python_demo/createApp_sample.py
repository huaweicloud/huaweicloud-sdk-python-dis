#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

appName="a"


def createApp_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r=cli.createApp(appName=appName)
        print(r.statusCode)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("start createApp")
    createApp_test()

