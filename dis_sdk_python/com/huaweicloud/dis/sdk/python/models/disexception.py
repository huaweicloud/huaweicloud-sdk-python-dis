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

    def __init__(self, errorMessage= "", resp_status=0, serviceErrMsg = ""):
        self.errorMessage = errorMessage
        self.respStatus = resp_status
        self.serviceErrMsg = serviceErrMsg


    def __str__(self):
        mes={"errorMessage": self.errorMessage,
            "respStatus":self.respStatus,
            "serviceErrMsg": self.serviceErrMsg}
        if not self.errorMessage:
            del mes['errorMessage']
        if not self.serviceErrMsg:
            del mes['serviceErrMsg']
        if self.respStatus==0:
            del mes["respStatus"]
        return json.dumps(mes, sort_keys=True)

    def getErrorType(self):
        """ return error code of exception
        
        :return: string, error code of exception.
        """
        return self.respStatus

    def getErrorMessage(self):
        """ return error message of exception
        
        :return: string, error message of exception.
        """
        return self.errorMessage
