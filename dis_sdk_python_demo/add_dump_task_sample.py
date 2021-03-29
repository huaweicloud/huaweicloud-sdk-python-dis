#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamname='1555064459865'
task_name='113'


basic_Schema=DumpTask.setSchema(key=['consumer_strategy','deliver_time_interval','agency_name','retry_duration'],
                                value=['LATEST', 30, 'dis_admin_agency',1800])


obs_dump_task =['destination_file_type','obs_bucket_path','file_prefix', 'partition_format','record_delimiter']
obs_Schema = DumpTask.setSchema(basic_Schema=basic_Schema,
                key=obs_dump_task,value=['text','obs-1253', '','yyyy', '|'])


def add_dump_task_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        # 添加OBS转储服务,配置osb_Schema值
        r = cli.add_dump_task(streamname, task_name,'OBS',obs_Schema)

        print(r.statusCode)
    except Exception as ex:
        print(str(ex))




if __name__ == '__main__':
    print("start add dump task")
    add_dump_task_test()











