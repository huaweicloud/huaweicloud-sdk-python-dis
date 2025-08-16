#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamName = "dis_test1"
streamId = "xxxxxxx"
appName = 'a'


def stream_consume_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r = cli.streamConsume(streamName, appName, streamId=streamId)
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("Use your Stream to query streamMonitor")
    stream_consume_test()
