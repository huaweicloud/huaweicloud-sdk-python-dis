#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

stream_name = "dis_test1"
label = 'total_put_records_per_stream'
start_time = 1546937556
end_time = 1546941516


def stream_monitor_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r = cli.streamMonitor(stream_name, label, start_time, end_time)
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("Use your Stream to query streamMonitor")
    stream_monitor_test()
