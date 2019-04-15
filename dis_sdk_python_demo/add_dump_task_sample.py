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


# mrs_dump_task=['destination_file_type','mrs_cluster_id','mrs_cluster_name','mrs_hdfs_path',
#                     'hdfs_prefix_folder','obs_bucket_path','file_prefix']
# mrs_Schema = DumpTask.setSchema(basic_Schema=basic_Schema,
#                 key=mrs_dump_task,value=['text','7d811b1b-cb40-4ddc-8995-8a992251cd44', 'mrs_7wu8','/app-logs',
#                                          '','obs-1253',''])


# dli_dump_task=['dli_database_name','dli_table_name','obs_bucket_path','file_prefix']
# dli_Schema = DumpTask.setSchema(basic_Schema=basic_Schema,
#                 key=dli_dump_task,value=['a','abcd_12345','obs-1253',''])


# dws_dump_task=['dws_cluster_name','dws_cluster_id','dws_database_name',
#                'dws_schema','dws_table_name','dws_delimiter',
#                'user_name','user_password',
#                'kms_user_key_name','kms_user_key_id',
#                'obs_bucket_path','file_prefix']
# dws_Schema = DumpTask.setSchema(basic_Schema=basic_Schema,
#                 key=dws_dump_task,value=['dis-to-dws','72d6a2e2-c6cf-4ca2-8e58-b6e3b0c89464', 'a',
#                                          'a','a','|',
#                                          'xxxx','abc#123456',
#                                          'dlf/default','7dbc8756-c274-4ad8-b9ae-0b43db2d3fe1',
#                                          'obs-1253', ''])


# CloudTable_HBase_dump_task=['cloudtable_cluster_name','cloudtable_cluster_id','cloudtable_table_name',
#                             'obs_backup_bucket_path','backup_file_prefix','cloudtable_row_key_delimiter',
#                             'row_key',
#                             'columns']
# CloudTable_HBase_Schema = DumpTask.setSchema(basic_Schema=basic_Schema,
#                 key=CloudTable_HBase_dump_task,
#                 value=['cloudtable_cluster','b8c095e2-db5f-4732-8a1d-eacd662e35dc', 'cloudtable_table',
#                            'obs-test-hz','','|',
#                                 [{"value": "dataId","type": "String"}],
#                                 [{"column_family_name": "cfname1","column_name": "ID","value": "dataId","type": "String"},
#                                  {"column_family_name": "cfname2","column_name": "VALUE","value": "dataValue","type": "String"}]
#                      ])


# CloudTable_OpenTSDB_dump_task=['cloudtable_cluster_name','cloudtable_cluster_id',
#                                'obs_backup_bucket_path', 'backup_file_prefix',
#                                'metric',
#                                'timestamp',
#                                'value',
#                                'tags']
# CloudTable_OpenTSDB_Schema = DumpTask.setSchema(basic_Schema=basic_Schema,
#                 key=CloudTable_OpenTSDB_dump_task,
#                 value=['cloudtable_cluster','b8c095e2-db5f-4732-8a1d-eacd662e35dc',
#                        'obs-test-hz','',
#                         [{"type":"Constant",
#                           "value":"age"}],
#                         {"value":"date","type":"String", "format":"yyyy/MM/dd HH:mm:ss"},
#                         {"value":"value","type":"Bigint"},
#                         [{"name":"name","value":"name","type":"Bigint"}]
#                  ])

def add_dump_task_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        # 添加OBS转储服务,配置osb_Schema值
        r = cli.add_dump_task(streamname, task_name,'OBS',obs_Schema)
        # 添加MRS转储服务,配置mrs_Schema值
        # r = cli.add_dump_task(streamname, task_name,'MRS',mrs_Schema)
        # 添加DLI转储任务,配置dli_Schema值
        # r = cli.add_dump_task(streamname, task_name, 'DLI', dli_Schema)
        # 添加DWS转储任务,配置dws_Schema值
        # r = cli.add_dump_task(streamname, task_name, 'DWS', dws_Schema)
        # 添加CloudTable HBase转储任务,配置CloudTable_HBase_Schema值
        # r = cli.add_dump_task(streamname, task_name, 'CloudTable_HBase', CloudTable_HBase_Schema)
        # 添加CloudTable OpenTSDB转储任务,配置CloudTable_OpenTSDB_Schema值
        # r = cli.add_dump_task(streamname, task_name, 'CloudTable_OpenTSDB', CloudTable_OpenTSDB_Schema)
        print(r.statusCode)
    except Exception as ex:
        print(str(ex))




if __name__ == '__main__':
    print("start add dump task")
    add_dump_task_test()











