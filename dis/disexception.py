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

#!/usr/bin/env python
# encoding: utf-8

import json


class DisException(Exception):
    """The Exception of the log request & response.
    
    :type errorType: string
    :param errorType: log service error code 
    
    :type errorMessage: string
    :param errorMessage: detailed information for the exception
    
    """

    def __init__(self, errorCode, errorMessage, resp_status=400, serviceErrCode = "", serviceErrMsg = ""):
        self._errorCode = errorCode
        self._errorMessage = errorMessage
        self.respStatus = resp_status
        self.serviceErrCode = serviceErrCode
        self.serviceErrMsg = serviceErrMsg


    def __str__(self):
        return json.dumps({
            "errorCode": self._errorCode,
            "errorMessage": self._errorMessage,
            "respStatus":self.respStatus,
            "serviceErrCode": self.serviceErrCode,
            "serviceErrMsg": self.serviceErrMsg
        }, sort_keys=True)

    def getErrorType(self):
        """ return error code of exception
        
        :return: string, error code of exception.
        """
        return self._errorCode

    def getErrorMessage(self):
        """ return error message of exception
        
        :return: string, error message of exception.
        """
        return self._errorMessage
