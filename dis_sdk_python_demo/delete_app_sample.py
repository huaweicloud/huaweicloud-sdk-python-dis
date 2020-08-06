#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

app_name = "a"


def delete_app_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r = cli.deleteApp(appName=app_name)
        print(r.statusCode)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("start deleteApp")
    delete_app_test()

