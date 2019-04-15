#!/usr/bin/python
# -*- coding:utf-8 -*-

SKIP_VERIFY_ATTR_TYPE = False

def _verify_attr_type(value, allowedAttrType):
    if isinstance(allowedAttrType, list):
        for t in allowedAttrType:
            if isinstance(value, t):
                return True
        return False
    return isinstance(value, allowedAttrType)

class _BaseModel(dict):

    def __init__(self, **kwargs):
        super(_BaseModel, self).__init__(**kwargs)


    def __getattr__(self, key):
        if key == 'allowedAttr':
            return {}
        key = key[:1].lower() + key[1:] if key is not None else ''
        if key in self.allowedAttr:
            return self.get(key)
        return None

    def __setattr__(self, key, value):
        key = key[:1].lower() + key[1:] if key is not None else ''
        if key in self.allowedAttr:
            flag = SKIP_VERIFY_ATTR_TYPE or _verify_attr_type(value, self.allowedAttr[key])
            if flag:
                self[key] = value

    def __delattr__(self, key):
        key = key[:1].lower() + key[1:] if key is not None else ''
        if key in self.allowedAttr:
            del self[key]
