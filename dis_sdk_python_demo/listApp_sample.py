#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

start_app_name=""

def listApp_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r=cli.listApp(start_app_name)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("Start Applist")
    listApp_test()

