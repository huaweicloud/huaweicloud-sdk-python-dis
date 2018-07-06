# Copyright 2002-2010 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
Created on 2018��4��21��

'''
import json
import urllib3
import requests
import base64
import dis.util as util
from dis import disrequest
from dis import disauth
from dis import disresponse
from dis import disadminresponse
from dis import disrecordresponse
from dis import discheckpointresponse
from dis.disexception import DisException

DEFAULT_QUERY_RETRY_COUNT = 10
DEFAULT_QUERY_RETRY_INTERVAL = 0.2

requests.packages.urllib3.disable_warnings()

class disclient(object):
    """ Construct the disclient with endpoint, ak, sk, projectid.

    :type endpoint: string
    :param endpoint: dis service host name and port, for example, dis.cn-north-1.myhuaweicloud.com:20004

    :type ak: string
    :param ak: hws accesskey

    :type sk: string
    :param sk: hws secretkey
    
    :type region: string
    :param region: the service deploy region    
    
    :type projectid: string
    :param projectid: hws project id for the user  
    
    : the user can get the ak/sk/projectid  from the hws,the user can refer https://support.huaweicloud.com/usermanual-dis/dis_01_0043.html
    """

    DIS_SDK_VERSION = '1.0.0'
    USER_AGENT = 'dis-python-sdk-v-' + DIS_SDK_VERSION
    TIME_OUT = 60

    def __init__(self, endpoint, ak, sk, projectid, region):
        self.endpoint = endpoint
        self.ak = ak
        self.sk = sk        
        self.projectid = projectid
        self.region = region
        self._timeout = self.TIME_OUT
        self._useragent = self.USER_AGENT
        
    def updateAuthInfo(self, ak, sk, projectid, region):
        self.ak = ak
        self.sk = sk        
        self.projectid = projectid
        self.region = region
        
    def setUserAgent(self, useragent):        
        self._useragent=useragent
        
        
    def __assert_to_validate(self, param, msg):
        param = util.safe_encode(param)
        if param is None or util.toString(param).strip() == '':
            raise Exception(msg)
        
        
    def _generateRequest(self, method, uri, query={}, headers={}, body="", userak="", usersk="", userxSecrityToken=""):
        req = disrequest.disRequest(method=method, host=self.endpoint, uri=uri, query=query, headers=headers, body=body)
        ak = self.ak
        sk = self.sk
        if userak is not "":
            ak = userak
        if usersk is not "":
            sk = usersk        
        #signer = disauth.Signer(self.ak, self.sk, self.region)
        signer = disauth.Signer(ak, sk, self.region)
        signer.Sign(req)
        req.headers["user-agent"]=self._useragent
        req.headers["Content-type"]="application/json"
        
        if userxSecrityToken is not "":
            req.headers["X-Security-Token"]=userxSecrityToken
            
        #print (req.__dict__)            
        
        if (headers):
            headers.update(req.headers)
            req.headers = headers
      
        return req
    
    def _getResponse(self, RawRequest):
        try:
            url = "https://" + self.endpoint + RawRequest.uri
            r = requests.request(RawRequest.method, url = url, params=RawRequest.query, data=RawRequest.body, headers=RawRequest.headers, timeout = self.TIME_OUT, verify=False)
            return r
        except Exception as ex:
            raise DisException('_sendRequest', str(ex))   
        
    def _sendRequest(self, rawRequest):
        r = self._getResponse(rawRequest)
        #print (r.__dict__)
        
        jsonResponse = {}
        if r.status_code >= 200 and r.status_code < 300:
            if r.content is not b'':
                jsonResponse = r.json() 
                #print (jsonResponse)
            return 200, jsonResponse 
        else:
            errMsg = ''
            errNo = ''
            if r._content is not b'':
                if r.status_code >= 500:
                    jsonResponse = r.json()
                    errMsg = jsonResponse["message"]
                    errNo  = jsonResponse["errorCode"]
                else:
                    errNo = str(r.status_code)
                    errMsg = str(r._content, 'utf-8')
            raise DisException("GetResponseErr", "the response is err", r.status_code, errNo, errMsg)

    
    def createStream(self, streamName, partitionCount, streamType="COMMON", ak="", sk="", xSecrityToken=""):
        
        '''
        create a dis stream . the stream captures and transport data records.
        
        you should specify the stream name ,the partition count and the streamtype
        
        the stream name is the id for the stream.it  Cannot repeat for a account of hws.
        
        the partition is the capacity for the stream. there are two types partition:COMMON and ADANCE
        
        the COMMON partition capacity is 1MB input per second, 1000 records input per second, 2MB output per second
        the ADVANCE partition capacity is 5MB input per second, 2000 records input per second, 10MB output per second
        
        the user specify the count and the type of partitions
        '''
        
        self.__assert_to_validate(streamName, "the stream Name is null")
        jsonBody = {"stream_name": streamName,
                    "partition_count": partitionCount,
                    "stream_type": streamType}
        jsonString = json.dumps(jsonBody)
        
        uri = "/v2/"+ self.projectid + "/streams/"
        req = self._generateRequest("POST", uri, body=jsonString, headers={}, query={}, userak=ak, usersk=sk, userxSecrityToken=xSecrityToken)


        (statusCode, responseData) = self._sendRequest(req)
        return disadminresponse.disCreateStreamResponse(statusCode, responseData)
    
    def deleteStream(self, streamName, ak="", sk="", xSecrityToken=""):
        '''
        delete a stream , all its partitions and records in the partitions.
        
        before deleting, you make sure all of the app operating the stream are closed 
        '''
        self.__assert_to_validate(streamName, "the stream Name is null")
        
        uri = "/v2/"+ self.projectid + "/streams/" + streamName
        req = self._generateRequest("DELETE", uri, headers={}, query={}, body="",userak=ak, usersk=sk, userxSecrityToken=xSecrityToken)

        (statusCode, responseData) = self._sendRequest(req)
        return disadminresponse.disDeleteStreamResponse(statusCode, responseData)
    
    def listStream(self, startStreamName="", limit = 0, ak="", sk="", xSecrityToken=""):
        '''
        list all of the stream of the user.
        
        the MAX of limit is 100,if larger than 100, the sdk should raise exception
        '''
        param = {}
       
        if startStreamName is not '':
            self.__assert_to_validate(startStreamName, "the stream Name is null")
            param["start_stream_name"]=startStreamName 
            
        if limit > 100:
            raise DisException("invalidparam", "the limit is to large")
        
        if limit != 0:
            param["limit"]=str(limit)
            
        #print (param)
            
        
        uri = "/v2/"+ self.projectid + "/streams/" 
        
        req = self._generateRequest("GET", uri, query=param, headers={}, body="", userak=ak, usersk=sk, userxSecrityToken=xSecrityToken)
        
        (statusCode, responseData) = self._sendRequest(req)
        return disadminresponse.disListStreamResponse(statusCode, responseData)  
    
    
    def describeStream(self, streamName, startPartitionId = "", limitPartitions = 0, ak="", sk="", xSecrityToken=""):
        '''
        get the detail of the specify stream.
        '''
        param = {}
       
        if startPartitionId is not '':
            param["start_partitionId"]=startPartitionId 
            
        if limitPartitions > 10000:
            raise DisException("invalidparam", "the limit is to large")
        
        if limitPartitions != 0:
            param["limit_partitions"]=str(limitPartitions)
            
        uri = "/v2/"+ self.projectid + "/streams/" + streamName + "/"
        
        req = self._generateRequest("GET", uri, query=param, headers={}, body="",userak=ak, usersk=sk, userxSecrityToken=xSecrityToken)
        
        (statusCode, responseData) = self._sendRequest(req)
        return disadminresponse.disDescribeStreamResponse(statusCode, responseData)  
    
    def putRecords(self, streamName, records, ak="", sk="", xSecrityToken=""):
        '''
        send records to the specify stream.
        
        :type streamName string
        :param streamName the streamName ID which want to send data
        
        :type records list
        :param records the data will be send,every one record MUST include two field: data and partition key.
        
        the data field is the RAW data will be sending to DIS.
        the partition_key field is the partition value, identify which partition should save the data
        '''
        
        
        for i in range(len(records)):
            if "data" in records[i].keys() and "partition_key" in records[i].keys():
                tempdata = base64.b64encode(records[i]["data"].encode('utf-8'))
                records[i]["data"] = str(tempdata, 'utf-8')
            else:
                raise DisException("InvalidParam", "the input records invalid")
        
        jsonBody = {"stream_name":streamName, "records": records}
        jsonString = json.dumps(jsonBody)
        #print (jsonString)
        
        uri = "/v2/"+ self.projectid + "/records/"
        req = self._generateRequest("POST", uri, body=jsonString, headers={}, query={}, userak=ak, usersk=sk, userxSecrityToken=xSecrityToken)
        
        (statusCode, responseData) = self._sendRequest(req)
        return disrecordresponse.disPutRecordsResponse(statusCode, responseData)          

    
    def getCursor(self, streamName, partitionId, cursorType, startSeq, ak="", sk="", xSecrityToken=""):
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
        
        if(cursorType != "AT_SEQUENCE_NUMBER" and cursorType != "AFTER_SEQUENCE_NUMBER" and cursorType != "TRIM_HORIZON" and cursorType != "LATEST"):
            raise DisException("Invalid param", "the cursor type is invalid")
        param["cursor-type"] = cursorType
            
        if(cursorType == "AT_SEQUENCE_NUMBER" and cursorType == "AFTER_SEQUENCE_NUMBER"):
            param["starting-sequence-number"] = startSeq

        uri = "/v2/"+ self.projectid + "/cursors/"

        req = self._generateRequest("GET", uri, query=param, headers={}, body="",userak=ak, usersk=sk, userxSecrityToken=xSecrityToken)
        
        (statusCode, responseData) = self._sendRequest(req)
        return disrecordresponse.disGetCursorResponse(statusCode, responseData)     
    
    def getRecords(self, partitioncursor, limit = 1000, ak="", sk="", xSecrityToken=""):
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
        
        
        params = {"partition-cursor": partitioncursor}
        
        if limit is not 0:
            params["limit"] = str(limit)
            
        uri = "/v2/"+ self.projectid + "/records/"
        req = self._generateRequest("GET", uri, query=params, headers={}, body="",userak=ak, usersk=sk, userxSecrityToken=xSecrityToken)
        (statusCode, responseData) = self._sendRequest(req)
        return disrecordresponse.disGetRecordsResponse(statusCode, responseData)           
        
        pass     
    

    def createApp(self, appName, ak="", sk="", xSecrityToken=""):
        jsonBody = {"app_name": appName}
        jsonString = json.dumps(jsonBody)
       
        uri = "/v2/"+ self.projectid + "/apps/"
        
        req = self._generateRequest("POST", uri, headers={}, query={}, body=jsonString, userak=ak, usersk=sk, userxSecrityToken=xSecrityToken)
        
        (statusCode, responseData) = self._sendRequest(req)
        return discheckpointresponse.disCreateAppResponse(statusCode, responseData)        
    
    def deleteApp(self, appName, ak="", sk="", xSecrityToken=""):
      
        uri = "/v2/"+ self.projectid + "/apps/" + appName + "/"
        
        req = self._generateRequest("DELETE", uri, headers={}, query={}, body="",userak=ak, usersk=sk, userxSecrityToken=xSecrityToken)
        
        (statusCode, responseData) = self._sendRequest(req)
        return discheckpointresponse.disDeleteAppResponse(statusCode, responseData)   
    
    def commitCheckpoint(self, streamName, appName, partitionId, seqNumber, metaData = "", checkpointType = "LAST_READ", ak="", sk="", xSecrityToken=""):
      
        uri = "/v2/"+ self.projectid + "/checkpoints/"
        
        jsonData = {"stream_name": streamName,
                    "app_name": appName,
                    "partition_id": partitionId,
                    "sequence_number": seqNumber,
                    "metadata": metaData,
                    "checkpoint_type":checkpointType}
        
        jsonStrig = json.dumps(jsonData)
        
        req = self._generateRequest("POST", uri, headers={}, query={}, body=jsonStrig, userak=ak, usersk=sk, userxSecrityToken=xSecrityToken)
        
        (statusCode, responseData) = self._sendRequest(req)
        return discheckpointresponse.disCommitCheckpointResponse(statusCode, responseData)  
    
    
    def getCheckpoint(self, streamName, appName, partitionId,  checkpointType = "LAST_READ", ak="", sk="", xSecrityToken=""):
      
        uri = "/v2/"+ self.projectid + "/checkpoints/"

        param = {"stream_name": streamName,
                "app_name": appName,
                "partition_id": partitionId,
                "checkpoint_type":checkpointType}
        
       
        req = self._generateRequest("GET", uri, query=param, headers={}, body="",userak=ak, usersk=sk, userxSecrityToken=xSecrityToken)
        
        (statusCode, responseData) = self._sendRequest(req)
        return discheckpointresponse.disGetCheckpointResponse(statusCode, responseData)

        