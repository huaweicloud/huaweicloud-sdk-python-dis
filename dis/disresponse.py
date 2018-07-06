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

'''
Created on 2018��4��23��

'''

class DisResponse(object):
    """ The base response class of all dis response. 
    :type status_code: int
    :param status_code: the http response code
    
    :type body: string
    :param body: HTTP response body, maybe empty
    """

    def __init__(self, status_code, body=''):
        if body is None:
            body = ''
        self.body = body
        self.statusCode = status_code

    def _getBody(self):
        """ Get body

        :return: string
        """
        return self.body
    
    def _getStatusCode(self):
        """ Get status code

        :return: int
        """
        return self.statusCode        

