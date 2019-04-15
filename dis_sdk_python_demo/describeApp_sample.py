#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

appname="a"

def describeApp_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r=cli.describeApp(appname)
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("Start describe App")
    describeApp_test()

