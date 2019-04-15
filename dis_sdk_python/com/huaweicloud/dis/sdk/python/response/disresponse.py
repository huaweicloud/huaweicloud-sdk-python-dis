#!/usr/bin/env python
# encoding: utf-8


class DisResponse(object):
    """ The base response class of all dis-sdk-resources-demo1 response.
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

