# Huawei Cloud DIS SDK for Python

Quick Links:
- [DIS Homepage](https://www.huaweicloud.com/en-us/product/dis.html), or Chinese language site [数据接入服务](https://www.huaweicloud.com/product/dis.html)

Installation
------------

The quick way:

    pip install huaweicloud-python-sdk-dis

Python Version
-------------------

Tested on Python 2.7, 3.3, 3.4, 3.5, 3.6 and pypy, Python 3.6 recommended

Usage
-----

    from dis_sdk_python import *
    cli = disclient(endpoint='**your-endpoint**',
                    ak='**your-ak**',
                    sk='**your-sk**',
                    projectid='**your-projectid**',
                    region='**your-region**')

    # ============================= create createStream =============================

    stream_name="my_stream_name"
    partition_count=1
    cli.createStream(stream_name,partition_count,data_type='JSON',stream_type='COMMON')

    # ============================= describeStream =============================

    streamname="my_stream_name"
    startPartitionId="shardId-0000000000"
    cli.describeStream(streamname, startPartitionId)

    # ============================= add_dump_task =============================

    streamname="my_stream_name"
    task_name="my_task_name"
    basic_Schema=DumpTask.setSchema(key=['consumer_strategy','deliver_time_interval','agency_name','retry_duration'],
                                value=['LATEST', 30, 'dis_admin_agency',1800])
    obs_dump_task =['destination_file_type','obs_bucket_path','file_prefix', 'partition_format','record_delimiter']
    obs_Schema = DumpTask.setSchema(basic_Schema=basic_Schema,
                    key=obs_dump_task,value=['text','obs-1253', '','yyyy', '|'])
    cli.add_dump_task(streamname, task_name,'OBS',obs_Schema)

    # ============================= describe_dump_task =============================

    streamname="my_stream_name"
    task_name="my_task_name"
    cli.describe_dump_task(streamname,task_name)

    # ============================= changepartitionQuantity=============================

    target_partition_count=2
    streamname="my_stream_name"
    cli.changepartitionQuantity(streamname,target_partition_count)

    # ============================= createApp =============================

    appName="my_appName"
    cli.createApp(appName)

    # ============================= describeApp =============================

    appName="my_appName"
    cli.describeApp(appName)

    # ============================= commitCheckpoint =============================

    streamname = "my_stream_name"
    appName="my_appName"
    partitionId="shardId-0000000000"
    seqNumber="0"
    cli.commitCheckpoint(streamname,appName,partitionId,seqNumber)

    # ============================= getCheckpoint =============================

    streamname = "my_stream_name"
    appName="my_appName"
    partitionId="shardId-0000000000"
    cli.getCheckpoint(streamname, appName, partitionId)

    # ============================= listStream  =============================

    start_stream_name = ""
    cli.listStream(start_stream_name)

    # ============================= list_dump_task =============================

    streamname = "my_stream_name"
    cli.list_dump_task(streamname)

    # ============================= listApp =============================

    start_app_name=""
    cli.listApp(start_app_name)

    # ============================= putRecords =============================

    streamname = "my_stream_name"
    records=[{"data":'{"a":"xxx4445"}', "partition_key": '0'}]
    cli.putRecords(streamname, records)

    # ============================= protobuf_putRecords =============================

    cli = disclient(endpoint='**your-endpoint**',
                ak='**your-ak**',
                sk='**your-sk**',
                projectid='**your-projectid**',
                region='**your-region**,
                bodySerializeType='protobuf')
    streamname = "my_stream_name"
    records=[{"data":'{"a":"xxx4445"}', "partition_key": '0'}]
    cli.putRecords(streamname,records)

    # ============================= getCursor =============================

    streamname = "my_stream_name"
    partitionId="shardId-0000000000"
    cli.getCursor(streamname, partitionId, cursorType='AT_SEQUENCE_NUMBER', startSeq="0")

    # ============================= getRecords =============================

    streamname = "my_stream_name"
    partitionId="shardId-0000000000"
    r = cli.getCursor(streamname, partitionId, cursorType='AT_SEQUENCE_NUMBER',startSeq="0")
    cli.getRecords(partitioncursor=r.cursor)

    # ============================= protobuf_getrecords =============================

    cli = disclient(endpoint='**your-endpoint**',
                ak='**your-ak**',
                sk='**your-sk**',
                projectid='**your-projectid**',
                region='**your-region**,
                bodySerializeType='protobuf')
    streamname = "my_stream_name"
    partitionId="shardId-0000000000"
    r = cli.getCursor(streamname, partitionId, cursorType='AT_SEQUENCE_NUMBER',startSeq="0")
    cli.getRecords(partitioncursor=r.cursor)

    # ============================= streamConsume =============================

    streamname = "my_stream_name"
    appName="my_appName"
    cli.streamConsume(streamname,appName)

    # ============================= streamMonitor =============================

    streamname = "my_stream_name"
    label='total_put_records_per_stream'
    start_time=1546937556
    end_time=1546941516
    cli.streamMonitor(streamname,label,start_time,end_time)

    # ============================= partitionMonitor =============================

    streamname = "my_stream_name"
    partition_id="shardId-0000000000"
    label='total_put_bytes_per_partition'
    start_time=1543376051
    end_time=1543389151
    cli.partitionMonitor(streamname,partition_id,label,start_time,end_time)

	# ============================= delete_dump_task =============================

    streamname="my_stream_name"
    task_name="my_task_name"
    cli.delete_dump_task(streamname, task_name)
	
	# ============================= deleteCheckpoint =============================
	
	streamname="my_stream_name"
    appName="my_appName"
    cli.deleteCheckpoint(streamname,appName)
	
	# ============================= deleteApp =============================

    appName="my_appName"
    cli.deleteApp(appName)
	
	# ============================= deleteStream =============================
	
	streamname="my_stream_name"
    cli.deleteStream(streamname)

Examples
-----------

see more examples in [examples](https://github.com/huaweicloud/huaweicloud-sdk-python-dis/tree/master/dis_sdk_python_demo)


Contributing
------------

For a development install, clone the repository and then install from
source:

    git clone https://github.com/huaweicloud/huaweicloud-sdk-python-dis.git


