#!/usr/bin/python
# -*- coding:utf-8 -*-
import base64
import json
import os
import sys
import time

import requests
import urllib3

from dis_sdk_python.com.huaweicloud.dis.sdk.python.models import disauth
from dis_sdk_python.com.huaweicloud.dis.sdk.python.models import disrequest
from dis_sdk_python.com.huaweicloud.dis.sdk.python.models.base_model import IS_PYTHON2, IS_PYTHON35_UP
from dis_sdk_python.com.huaweicloud.dis.sdk.python.models.disexception import DisException
from dis_sdk_python.com.huaweicloud.dis.sdk.python.models.log import log
from dis_sdk_python.com.huaweicloud.dis.sdk.python.response import disAppresonse
from dis_sdk_python.com.huaweicloud.dis.sdk.python.response import disConsumeresponse
from dis_sdk_python.com.huaweicloud.dis.sdk.python.response import disGetresponse
from dis_sdk_python.com.huaweicloud.dis.sdk.python.response import disMonitorresponse
from dis_sdk_python.com.huaweicloud.dis.sdk.python.response import disStreamresponse
from dis_sdk_python.com.huaweicloud.dis.sdk.python.response import discheckpointresponse
from dis_sdk_python.com.huaweicloud.dis.sdk.python.response import disrecordresponse
from dis_sdk_python.com.huaweicloud.dis.sdk.python.utils import util


DEFAULT_QUERY_RETRY_COUNT = 10
DEFAULT_RECORDS_RETRY_COUNT = 20
# DEFAULT_QUERY_RETRY_INTERVAL=0.2

RECORDS_RETRIES = 20
EXCEPTION_RETRIES = 10
stream_mes = {}


if IS_PYTHON2:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class disclient(object):
    """ Construct the disclient with endpoint, ak, sk, projectid.

    :type endpoint: string
    :param endpoint: dis-sdk-resources-demo1 service host name and port, for example, dis-sdk-resources-demo1.cn-north-1.myhuaweicloud.com:20004

    :type ak: string
    :param ak: hws accesskey

    :type sk: string
    :param sk: hws secretkey

    :type region: string
    :param region: the service deploy region

    :type projectid: string
    :param projectid: hws project id for the user

    : the user can get the ak/sk/projectid  from the hws,the user can refer https://support.huaweicloud.com/usermanual-dis-sdk-resources-demo1/dis_01_0043.html
    """

    DIS_SDK_VERSION = '2.0.0'
    USER_AGENT = 'dis-python-sdk-v-' + DIS_SDK_VERSION
    TIME_OUT = 60

    def __init__(self, endpoint, ak, sk, projectid, region, bodySerializeType=''):
        self.endpoint = endpoint
        if not endpoint.startswith("http"):
            self.endpoint = "https://" + endpoint
        self.host = endpoint.split("//")[-1]
        self.ak = ak
        self.sk = sk
        self.projectid = projectid
        self.region = region
        self.bodySerializeType = bodySerializeType
        self._timeout = self.TIME_OUT
        self._useragent = self.USER_AGENT
        self.result = []

    def updateAuthInfo(self, ak, sk, projectid, region):
        self.ak = ak
        self.sk = sk
        self.projectid = projectid
        self.region = region

    def setUserAgent(self, useragent):
        self._useragent = useragent

    def __assert_to_validate(self, param, msg):
        param = util.safe_encode(param)
        if param is None or util.toString(param).strip() == '' or param == b'':
            raise Exception(msg)

    def __generateRequest(self, method, uri, query={}, headers={}, body="", userak="", usersk="", userxSecrityToken=""):
        req = disrequest.disRequest(method=method, host=self.host, uri=uri, query=query, headers=headers, body=body)
        ak = self.ak
        sk = self.sk
        if userak is not "":
            ak = userak
        if usersk is not "":
            sk = usersk
        signer = disauth.Signer(ak, sk, self.region)
        signer.Sign(req)
        req.headers["user-agent"] = self._useragent
        req.headers["Content-Type"] = "application/json; charset=UTF-8"

        # req.headers['Connection']='keep-alive'
        # req.headers['Content-Length'] = '250'

        if userxSecrityToken is not "":
            req.headers["X-Security-Token"] = userxSecrityToken

        if (headers):
            headers.update(req.headers)
            req.headers = headers
        # print(req.__dict__)
        return req

    def __sendRequest(self, rawRequest):
        retryCount = 0
        url = self.endpoint + rawRequest.uri
        wait=0.05
        while retryCount <= DEFAULT_QUERY_RETRY_COUNT:
            try:
                if retryCount != 0:
                    time.sleep(wait)
                    wait = wait * 2
                    rawRequest.headers.pop(disauth.HeaderXDate)
                    rawRequest.headers.pop(disauth.HeaderAuthorization)
                    disauth.Signer(self.ak, self.sk, self.region).Sign(rawRequest)
                r = requests.request(method=rawRequest.method, url=url, params=rawRequest.query, data=rawRequest.body,
                                     headers=rawRequest.headers, timeout=self.TIME_OUT, verify=False)

                if r.status_code >= 200 and r.status_code < 300:
                    try:jsonResponse = json.loads(r.content)
                    except:jsonResponse = r.content
                    return r.status_code, jsonResponse

                else:
                    errNo = r.status_code
                    try:
                        errMsg = json.loads(r.content)
                    except:
                        errMsg=r.content
                    raise DisException(str(errMsg),errNo)

            except Exception as ex:
                if retryCount < DEFAULT_QUERY_RETRY_COUNT and \
                        (type(ex) == DisException and ex.respStatus >= 500
                         or "connect timeout" in str(ex)
                         or ("read timeout" in str(ex) and rawRequest.method == "GET")):
                    log("Find Retriable Exception [" + str(
                        ex) + "], url [" + rawRequest.method + " " + rawRequest.uri + "], currRetryCount is " + str(
                        retryCount))
                    retryCount = retryCount + 1
                else:
                    if type(ex) == DisException:
                        raise DisException(ex.errorMessage)
                    else:
                        raise DisException(str(ex))

    def createStream(self, stream_name,partition_count,data_type,stream_type,data_duration=24):

        '''
        create a dis-sdk-resources-demo1 stream . the stream captures and transport data records.

        you should specify the stream name ,the partition count and the streamtype

        the stream name is the id for the stream.it  Cannot repeat for a account of hws.

        the partition is the capacity for the stream. there are two types partition:COMMON and ADANCE

        the COMMON partition capacity is 1MB input per second, 1000 records input per second, 2MB output per second
        the ADVANCE partition capacity is 5MB input per second, 2000 records input per second, 10MB output per second

        the user specify the count and the type of partitions
        '''

        kwargs={
                "stream_name": stream_name,
                "partition_count": partition_count,
                "stream_type": stream_type,
                "data_type":data_type,
                "data_duration": data_duration
            }
        jsonString = json.dumps(kwargs)
        uri = "/v2/" + self.projectid + "/streams/"
        req = self.__generateRequest("POST", uri, body=jsonString, headers={}, query={})

        (statusCode, responseData) = self.__sendRequest(req)
        return disStreamresponse.disCreateStreamResponse(statusCode, responseData)

    def __getDumpTask(self,task_name,dump_task_type,kwargs):
        jsonbody = {"destination_type": dump_task_type}
        if dump_task_type.startswith('CloudTable'):
            jsonbody['destination_type']=(dump_task_type.split('_')[0]).upper()
        kwargs['task_name']=task_name
        if dump_task_type == 'OBS':
            jsonbody['obs_destination_descriptor']=kwargs
        elif dump_task_type == 'MRS':
            jsonbody['mrs_destination_descriptor']=kwargs
        elif dump_task_type == 'DLI':
            jsonbody['dli_destination_descriptor']=kwargs
        elif dump_task_type == 'CloudTable_HBase':
            cloudtable_schema={}
            cloudtable_schema['row_key']=kwargs['row_key']
            cloudtable_schema['columns'] = kwargs['columns']
            kwargs['cloudtable_schema']=cloudtable_schema
            del kwargs['row_key'],kwargs['columns']
            jsonbody['cloudtable_destination_descriptor'] = kwargs
        elif dump_task_type == 'CloudTable_OpenTSDB':
            opentsdb_schema={}
            opentsdb_schema['metric']= kwargs['metric']
            opentsdb_schema['timestamp'] = kwargs['timestamp']
            opentsdb_schema['value'] = kwargs['value']
            opentsdb_schema['tags'] = kwargs['tags']
            kwargs['opentsdb_schema'] = [opentsdb_schema]
            del kwargs['metric'],kwargs['timestamp'],kwargs['value'],kwargs['tags']
            jsonbody['cloudtable_destination_descriptor'] = kwargs
        else:
            jsonbody['dws_destination_descriptor'] = kwargs
        return jsonbody


    def add_dump_task(self, stream_name,task_name,dump_task_type,kwargs):
        jsonbody=self.__getDumpTask(task_name,dump_task_type,kwargs)
        jsonString = json.dumps(jsonbody)
        uri = "/v2/" + self.projectid + "/stream/" + stream_name + '/transfer-tasks/'
        req = self.__generateRequest("POST", uri, body=jsonString, headers={}, query={})
        (statusCode, responseData) = self.__sendRequest(req)
        return disStreamresponse.disCreateStreamResponse(statusCode, responseData)

    def deleteStream(self, streamName, ak="", sk="", xSecrityToken=""):
        '''
        delete a stream , all its partitions and records in the partitions.

        before deleting, you make sure all of the app operating the stream are closed
        '''

        uri = "/v2/" + self.projectid + "/streams/" + streamName
        req = self.__generateRequest("DELETE", uri, headers={}, query={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return disStreamresponse.disDeleteResponse(statusCode, responseData)

    def delete_dump_task(self, streamName, task_name='', ak="", sk="", xSecrityToken=""):

        uri = "/v2/" + self.projectid + "/streams/" + streamName + "/transfer-tasks/" + task_name + '/'
        req = self.__generateRequest("DELETE", uri, headers={}, query={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return disStreamresponse.disDeleteResponse(statusCode, responseData)

    def listStream(self, startStreamName="", limit=100, ak="", sk="", xSecrityToken=""):
        '''
        list all of the stream of the user.

        the MAX of limit is 100,if larger than 100, the sdk should raise exception
        '''

        param = {}
        if startStreamName.strip():
            param["start_stream_name"] = startStreamName

        param["limit"] = limit

        uri = "/v2/" + self.projectid + "/streams/"
        req = self.__generateRequest("GET", uri, query=param, headers={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        if 'stream_info_list' in responseData.keys():
            del responseData['stream_info_list']
        return disStreamresponse.disListStreamResponse(statusCode, responseData)

    def describeStream(self, streamName, startPartitionId="", limitPartitions=1000, ak="", sk="", xSecrityToken=""):

        param = {}
        if startPartitionId.strip():
            param["start_partitionId"] = startPartitionId

        param["limit_partitions"] = limitPartitions

        uri = "/v2/" + self.projectid + "/streams/" + streamName

        req = self.__generateRequest("GET", uri, query=param, headers={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return disStreamresponse.disDescribeStreamResponse(statusCode, responseData)

    def list_dump_task(self, streamName, ak="", sk="", xSecrityToken=""):

        uri = "/v2/" + self.projectid + "/streams/" + streamName + "/" + "transfer-tasks/"

        req = self.__generateRequest("GET", uri, headers={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return disStreamresponse.dislistdumptaskResponse(statusCode, responseData)

    def describe_dump_task(self, streamName, task_name, ak="", sk="", xSecrityToken=""):

        uri = "/v2/" + self.projectid + "/stream/" + streamName + "/" + "transfer-tasks/" + task_name

        req = self.__generateRequest("GET", uri, headers={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return disStreamresponse.disdescribedumptaskResponse(statusCode, responseData)

    def __sendRecords(self, streamName, streamId, records, ak="", sk="", xSecrityToken=""):
        '''
        send records to the specify stream.

        :type streamName string
        :param streamName the streamName ID which want to send data

        :type records list
        :param records the data will be send,every one record MUST include two field: data and partition key.

        the data field is the RAW data will be sending to DIS.
        the partition_key field is the partition value, identify which partition should save the data
        '''

        if self.bodySerializeType:
            from dis_sdk_python.com.huaweicloud.dis.sdk.python.proto import record_pb2
            p = record_pb2.PutRecordsRequest()
            p.streamName = streamName
            p.streamId = streamId
            for j in records:
                p1 = p.records.add()
                if j.get('partition_key') != None:
                    p1.partitionKey = j.get('partition_key')

                if j.get('partition_id') != None:
                    p1.partitionId = j.get('partition_id')

                if j.get('explicit_hash_key') != None:
                    p1.explicitHashKey  = j.get('explicit_hash_key')

                if IS_PYTHON2:
                    p1.data = bytes(str(j.get('data')))
                else:
                    p1.data = bytes(str(j.get('data')), encoding='utf-8')
            jsonString = p.SerializeToString()
        else:
            def data_Base64(data):
                import copy
                data1=copy.deepcopy(data)
                if IS_PYTHON2:
                    data1['data'] = base64.b64encode(str(data1.get('data')))
                else:
                    tempdata = base64.b64encode(bytes(str(data1.get('data')), encoding='utf-8'))
                    data1['data'] = str(tempdata, 'utf-8')
                return data1
            records=list(map(data_Base64, records))
            jsonBody = {"stream_name": streamName, "stream_id": streamId, "records": records}
            jsonString = json.dumps(jsonBody)


        uri = "/v2/" + self.projectid + "/records/"
        req = self.__generateRequest("POST", uri, body=jsonString, headers={}, query={}, userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)
        if self.bodySerializeType:
            req.headers["Content-Type"] = "application/x-protobuf;charset=utf-8"

        (statusCode, responseData) = self.__sendRequest(req)
        return disrecordresponse.disPutRecordsResponse(statusCode, responseData)

    def __list_of_groups(self, init_list, childern_list_len):
        list_of_group = zip(*(iter(init_list),) * childern_list_len)
        end_list = [list(i) for i in list_of_group]
        count = len(init_list) % childern_list_len
        end_list.append(init_list[-count:]) if count != 0 else end_list
        return end_list

    def __Refine_data(self, stream_name, stream_id, records):
        totalPutRecordsResultEntryList = {}
        totalPutRecordsResultEntryList['failed_record_count'] = 0
        totalPutRecordsResultEntryList['records'] = []
        rangeRecords = records
        putRecordsResultEntryList = None
        retryIndex = None
        retryPutRecordsRequest = rangeRecords
        retryCount = -1
        currentFailed = 0
        wait = 0.05
        while retryCount < RECORDS_RETRIES and (retryIndex is None or len(retryIndex) > 0):
            if retryCount != -1:
                time.sleep(wait)
                wait = wait * 2
            r = self.__sendRecords(stream_name, stream_id, retryPutRecordsRequest)
            currentFailed = r.failedRecordCount
            # print("%s: send %s records,failed %s records,retryCount %s" % (
            # streamname, len(retryPutRecordsRequest), currentFailed, retryCount + 1))

            if putRecordsResultEntryList is None and currentFailed == 0 or RECORDS_RETRIES == 0:
                retryIndex = [-1 for temp in range(currentFailed)]
                putRecordsResultEntryList = r.recordResult
                break

            if putRecordsResultEntryList is None:
                putRecordsResultEntryList = [None for temp in range(len(rangeRecords))]

            retryIndexTemp = []

            if currentFailed > 0:
                retryPutRecordsRequest = []

            for j in range(0, len(r.recordResult)):
                if retryIndex:
                    originalIndex = retryIndex[j]
                else:
                    originalIndex = j
                putRecordsResultEntry = r.recordResult[j]

                error_code = putRecordsResultEntry.get('error_code')
                if error_code and (error_code == 'DIS.4303' or error_code == 'DIS.5250'):
                    retryIndexTemp.append(originalIndex)
                    retryPutRecordsRequest.append(rangeRecords[originalIndex])

                if error_code and error_code != 'DIS.4303' and error_code != 'DIS.5250':
                    totalPutRecordsResultEntryList["failed_record_count"] += 1

                putRecordsResultEntryList[originalIndex] = putRecordsResultEntry

            if len(retryIndexTemp) > 0:
                retryIndex = retryIndexTemp
            else:
                retryIndex = []
            retryCount += 1

        totalPutRecordsResultEntryList["failed_record_count"] += len(retryIndex)
        totalPutRecordsResultEntryList["records"].extend(putRecordsResultEntryList)
        Faile_count = int(totalPutRecordsResultEntryList.get('failed_record_count'))
        log('{}{}:send {} records,failed {} records'.format(stream_name, stream_id, len(records), Faile_count), 'info')
        return totalPutRecordsResultEntryList

    def putRecords(self, streamname, records):
        if not stream_mes.get(streamname):
            try:
                r = self.describeStream(streamname)
                if r.statusCode == 200:
                    stream_type = r.streamType
                    partitions = len([i for i in r.partitions if i.get('status') == 'ACTIVE'])
                    stream_mes[streamname] = {"stream_type": stream_type, "partitions": partitions}
            except Exception as ex:
                print(str(ex))
        partitioncount = stream_mes.get(streamname).get('partitions')
        if stream_mes.get(streamname).get("stream_type") == 'COMMON':
            end_list = self.__list_of_groups(records, partitioncount * 1000)
        else:
            end_list = self.__list_of_groups(records, partitioncount * 2000)

        totalPutRecordsResultEntryList = {}
        totalPutRecordsResultEntryList['failed_record_count'] = 0
        totalPutRecordsResultEntryList['records'] = []
        limitBytes = 4 * 1024 * 1024
        new_records = []
        for i in range(0, len(end_list)):
            while end_list[i]:
                b = []
                curBytes = 0
                for k in end_list[i]:
                    b.append(k)
                    itemLen = len(str(k))
                    curBytes += itemLen
                    if curBytes <= limitBytes:
                        continue
                    else:
                        if len(b) > 1:
                            b.pop()
                            curBytes -= itemLen
                        break
                new_records.append(b)
                end_list[i] = end_list[i][len(b):]
        for j in range(0, len(new_records)):
            rangeRecords = new_records[j]
            r = self.__Refine_data(streamname, "", rangeRecords)
            totalPutRecordsResultEntryList['failed_record_count'] += r['failed_record_count']
            totalPutRecordsResultEntryList['records'].extend(r['records'])
        return disrecordresponse.disPutRecordsResponse(200, totalPutRecordsResultEntryList)

    def put_records(self, stream_name, stream_id, records):
        """
        support authorization scenarios use stream_id
        stream_name is mandatory parameter, can be an empty string.
        stream_id is mandatory parameter, can be an empty string.
        stream_name and stream_id can not both be empty string.
        use stream_name when both not be empty string
        :param stream_name: stream name
        :param stream_id: stream id
        :param records: records
        :return:
        """
        totalPutRecordsResultEntryList = {}
        totalPutRecordsResultEntryList['failed_record_count'] = 0
        totalPutRecordsResultEntryList['records'] = []
        r = self.__Refine_data(stream_name, stream_id, records)
        totalPutRecordsResultEntryList['failed_record_count'] += r['failed_record_count']
        totalPutRecordsResultEntryList['records'].extend(r['records'])
        return disrecordresponse.disPutRecordsResponse(200, totalPutRecordsResultEntryList)

    def getCursor(self, streamName, partitionId, cursorType, startSeq='', timestamp='',ak="", sk="", xSecrityToken=""):
        '''
        the cursor is the pointer to get the data in partition.

        :type streamName string
        :param streamName the streamName ID which want to send data

        :type partitionId string
        :param partitionId the partition ID which want to get data, you can get all of the partition info from describeStream interface

        :type cursorType string
        :param cursorType. there are four type for the cursor
            :AT_SEQUENCE_NUMBER  The consumer application starts reading from the position denoted by a specific sequence number. This is the default Cursor Type.
            :AFTER_SEQUENCE_NUMBER The consumer application starts reading right after the position denoted by a specific sequence number.
            :TRIM_HORIZON  The consumer application starts reading at the last untrimmed record in the partition in the system, which is the oldest data record in the partition.
            :LATEST  Start reading just after the most recent record in the partition, so that you always read the most recent data in the partition


        :type startSeq tring
        :param startSeq
           Sequence number of the data record in the partition from which to start reading.
           Value range: 0 to 9223372036854775807
           Each data record has a sequence number that is unique within its partition. The sequence number is assigned by DIS when a data producer calls PutRecords to add data to a DIS stream.
           Sequence numbers for the same partition key generally increase over time; the longer the time period between write requests (PutRecords requests), the larger the sequence numbers become.
        '''
        param = {}
        param["stream-name"] = streamName
        param["partition-id"] = partitionId
        param["cursor-type"] = cursorType
        if startSeq.strip():
            param["starting-sequence-number"] = startSeq
        if timestamp:
            param["timestamp"] = timestamp

        uri = "/v2/" + self.projectid + "/cursors/"

        req = self.__generateRequest("GET", uri, query=param, headers={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return disrecordresponse.disGetCursorResponse(statusCode, responseData)

    def getRecords(self, partitioncursor, limit=1000, ak="", sk="", xSecrityToken=""):
        '''
        :type partitioncursor string
        :param partitioncursor: you can get the cursor from getCursor interface
            Cursor, which specifies the position in the partition from which to start reading data records sequentially.
            Value: 1 to 512 characters

        :type limit int
        :param limit :The maximum number of records to return.
            Value range: 1 to 10000
            Default value: 1000
        '''
        params={}
        params["partition-cursor"]=partitioncursor
        params["limit"] = limit

        uri = "/v2/" + self.projectid + "/records/"
        req = self.__generateRequest("GET", uri, query=params, headers={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)
        if self.bodySerializeType:
            req.headers["Content-Type"] = "application/x-protobuf;charset=utf-8"

        (statusCode, responseData) = self.__sendRequest(req)
        return disrecordresponse.disGetRecordsResponse(statusCode, responseData)

    def createApp(self, appName, ak="", sk="", xSecrityToken=""):

        jsonBody = {"app_name": appName}
        jsonString = json.dumps(jsonBody)

        uri = "/v2/" + self.projectid + "/apps/"

        req = self.__generateRequest("POST", uri, headers={}, query={}, body=jsonString, userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return disAppresonse.disCreateAppResponse(statusCode, responseData)

    def describeApp(self, appName, ak="", sk="", xSecrityToken=""):

        uri = "/v2/" + self.projectid + "/apps/" + appName
        req = self.__generateRequest("GET", uri, headers={}, query={}, userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)
        (statusCode, responseData) = self.__sendRequest(req)
        return disAppresonse.disdescribeAppResponse(statusCode, responseData)

    def listApp(self, appName, ak="", sk="", xSecrityToken="", limit=100):

        param = {}
        param["limit"] = limit

        if appName.strip():
            param["start_app_name"] = appName

        uri = "/v2/" + self.projectid + "/apps"

        req = self.__generateRequest("GET", uri, headers={}, query=param, userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return disAppresonse.disApplistResponse(statusCode, responseData)

    def deleteApp(self, appName, ak="", sk="", xSecrityToken=""):

        uri = "/v2/" + self.projectid + "/apps/" + appName + "/"
        req = self.__generateRequest("DELETE", uri, headers={}, query={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return disAppresonse.disDeleteAppResponse(statusCode, responseData)

    def commitCheckpoint(self, streamName, appName, partitionId, seqNumber, metaData="", checkpointType="LAST_READ",
                         ak="", sk="", xSecrityToken=""):

        uri = "/v2/" + self.projectid + "/checkpoints/"

        jsonData = {"stream_name": streamName,
                    "app_name": appName,
                    "partition_id": partitionId,
                    "sequence_number": seqNumber,
                    "metadata": metaData,
                    "checkpoint_type": checkpointType}

        jsonStrig = json.dumps(jsonData)

        req = self.__generateRequest("POST", uri, headers={}, query={}, body=jsonStrig, userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return discheckpointresponse.disCommitCheckpointResponse(statusCode, responseData)

    def getCheckpoint(self, streamName, appName, partitionId, checkpointType="LAST_READ", ak="", sk="",
                      xSecrityToken=""):

        param = {"stream_name": streamName,
                 "app_name": appName,
                 "partition_id": partitionId,
                 "checkpoint_type": checkpointType}

        uri = "/v2/" + self.projectid + "/checkpoints/"

        req = self.__generateRequest("GET", uri, query=param, headers={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)
        (statusCode, responseData) = self.__sendRequest(req)
        return discheckpointresponse.disGetCheckpointResponse(statusCode, responseData)

    def deleteCheckpoint(self, streamName, appName, ak="", sk="", xSecrityToken=""):

        param={}
        param['stream_name']=streamName
        param['app_name'] = appName

        uri = "/v2/" + self.projectid + "/checkpoints/"
        req = self.__generateRequest("DELETE", uri, query=param, headers={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return discheckpointresponse.disdeleteCheckpointResponse(statusCode, responseData)

    def changepartitionQuantity(self, stream_name_test, target_partition_count, ak="", sk="", xSecrityToken=""):

        jsonBody = {
            "stream_name": stream_name_test,
            "target_partition_count": target_partition_count
        }
        jsonString = json.dumps(jsonBody)

        uri = "/v2/" + self.projectid + "/streams/" + stream_name_test
        req = self.__generateRequest("PUT", uri, headers={}, body=jsonString, userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)
        (statusCode, responseData) = self.__sendRequest(req)
        return disGetresponse.dischangepartitionCountResponse(statusCode, responseData)

    def streamConsume(self, streamName, appName, checkpoint_type='LAST_READ', start_partition_id=0, limit=10, ak="",
                      sk="", xSecrityToken=""):

        param={}
        param['start_partition_id']=start_partition_id
        param['checkpoint_type'] = checkpoint_type
        param['limit'] = limit

        uri = "/v2/" + self.projectid + '/apps/' + appName + '/streams/' + streamName
        req = self.__generateRequest("GET", uri, query=param, headers={}, body="", userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return disConsumeresponse.disGetConsumeresponse(statusCode, responseData)

    def streamMonitor(self, stream_name, label, start_time='', end_time='', ak="", sk="", xSecrityToken=""):

        param = {}
        param["label"] = label
        param["end_time"] = end_time
        param["start_time"] = start_time

        jsonData = {"stream_name": stream_name}
        jsonStrig = json.dumps(jsonData)
        uri = "/v2/" + self.projectid + "/streams/" + stream_name + '/metrics'
        req = self.__generateRequest("GET", uri, query=param, headers={}, body=jsonStrig, userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)
        (statusCode, responseData) = self.__sendRequest(req)
        return disMonitorresponse.disGetMonitorResponse(statusCode, responseData)

    def partitionMonitor(self, stream_name, partitionId, label, start_time, end_time, ak="", sk="", xSecrityToken=""):

        param = {}
        param["label"] = label
        param["start_time"] = start_time
        param["end_time"] = end_time

        jsonData = {"stream_name": stream_name,
                    "partition_id": partitionId
                    }
        jsonStrig = json.dumps(jsonData)
        uri = "/v2/" + self.projectid + "/streams/" + stream_name + '/partitions/' + partitionId + '/metrics'
        req = self.__generateRequest("GET", uri, query=param, headers={}, body=jsonStrig, userak=ak, usersk=sk,
                                     userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self.__sendRequest(req)
        return disMonitorresponse.disGetMonitorResponse(statusCode, responseData)









