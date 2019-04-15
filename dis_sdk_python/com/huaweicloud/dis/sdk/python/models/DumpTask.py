#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python.com.huaweicloud.dis.sdk.python.models.disexception import DisException
def setSchema(key,value,basic_Schema={}):
    if len(key)==len(value):
        Schema=dict(list(zip(key,value)))
        basic_Schema.update(Schema)
        return basic_Schema
    else:
        raise DisException('key and value Different lengths')




