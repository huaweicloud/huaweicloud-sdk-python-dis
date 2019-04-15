#!/usr/bin/python
# -*- coding:utf-8 -*-

def safe_encode(item):
    if isinstance(item, str):
        try:
            item = item.encode('UTF-8')
        except UnicodeDecodeError:
            try:
                item = item.encode('GB2312')
            except Exception:
                item = None
    return item

def toString(item):
    try:
        return str(item) if item is not None else ''
    except Exception:
        return ''
    
def validateString(item, maxlen):
    if (len(item) >= maxlen):
        return -1
    return ''