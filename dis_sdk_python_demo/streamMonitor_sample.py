#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamname = "dis_test1"
label='total_put_records_per_stream'
start_time=1546937556
end_time=1546941516

def streamMonitor_test():
    cli = disclient(endpoint='',ak='',sk='',projectid='',region='')
    try:
        r=cli.streamMonitor(streamname,label,start_time,end_time)
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)
    except Exception as ex:
        print(str(ex))



if __name__ == '__main__':
    print("Use your Stream to query streamMonitor")
    streamMonitor_test()







