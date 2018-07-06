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
Created on 2018��4��24��
'''

from dis.disresponse import DisResponse

class disCreateAppResponse(DisResponse):
    
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body)
        
class disDeleteAppResponse(DisResponse):
    
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body)
        
class disCommitCheckpointResponse(DisResponse):
    
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body) 
        
class disGetCheckpointResponse(DisResponse):
    
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body)   
        self.seqNumber = body["sequence_number"]  
        self.metaData = body["metaData"]
        
    def _printResponse(self):
        print ("GetCheckpointResponse")
        print ("seqNumber: %s" %(self.seqNumber))
        print ("metadata: %s" %(self.metaData))