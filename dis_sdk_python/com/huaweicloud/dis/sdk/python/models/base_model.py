import os
import platform
import sys

IS_WINDOWS = platform.system() == 'Windows' or os.name == 'nt'

IS_PYTHON2 = sys.version_info.major == 2 or sys.version < '3'
IS_PYTHON35_UP = sys.version >= '3.5'
BASESTRING = basestring if IS_PYTHON2 else str

UNICODE = unicode if IS_PYTHON2 else str

LONG = long if IS_PYTHON2 else int

if IS_PYTHON2:
    from dis_sdk_python.com.huaweicloud.dis.sdk.python.models.model_python2 import _BaseModel
else:
    from dis_sdk_python.com.huaweicloud.dis.sdk.python.models.model_python3 import _BaseModel

BaseModel = _BaseModel