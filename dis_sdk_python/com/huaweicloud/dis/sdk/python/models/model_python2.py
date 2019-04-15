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

class _BaseModelMetaClass(type):

    def __new__(cls, name, bases, attrs):
        if name == 'BaseModel':
            return type.__new__(cls, name, bases, attrs)
        if 'allowedAttr' in attrs and isinstance(attrs['allowedAttr'], dict):
            allowedAttr = attrs['allowedAttr']
            def get_method(self, key):
                key = key[:1].lower() + key[1:] if key is not None else ''
                if key in allowedAttr:
                    return self.get(key)
                return None

            def set_method(self, key, value):
                key = key[:1].lower() + key[1:] if key is not None else ''
                if key in allowedAttr:
                    flag = SKIP_VERIFY_ATTR_TYPE or _verify_attr_type(value, allowedAttr[key])
                    if flag:
                        self[key] = value

            def del_method(self, key):
                key = key[:1].lower() + key[1:] if key is not None else ''
                if key in allowedAttr:
                    del self[key]

            attrs['__getattr__'] = get_method
            attrs['__setattr__'] = set_method
            attrs['__delattr__'] = del_method

            del attrs['allowedAttr']

        return type.__new__(cls, name, bases, attrs)

class _BaseModel(dict):
    __metaclass__ = _BaseModelMetaClass

    def __init__(self, **kwargs):
        super(_BaseModel, self).__init__(**kwargs)
