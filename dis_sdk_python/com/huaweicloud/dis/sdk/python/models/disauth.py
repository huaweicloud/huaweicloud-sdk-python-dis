#!/usr/bin/python
# -*- coding:utf-8 -*-

import binascii
import hashlib
import hmac
from datetime import datetime

from dis_sdk_python.com.huaweicloud.dis.sdk.python.models.base_model import IS_PYTHON2, IS_PYTHON35_UP

if IS_PYTHON2:
    from urllib import quote
if IS_PYTHON35_UP:
    from urllib.parse import quote

# BasicDateFormat and BasicDateFormatShort define aws-date format
BasicDateFormat = "%Y%m%dT%H%M%SZ"
BasicDateFormatShort = "%Y%m%d"
TerminationString = "sdk_request"
Algorithm = "SDK-HMAC-SHA256"
PreSKString = "SDK"
HeaderXDate = "x-sdk-date"
HeaderDate = "date"
HeaderHost = "host"
HeaderAuthorization = "Authorization"
HeaderContentSha256 = "x-sdk-content-sha256"


def urlencode(s):
    return quote(str(s), safe='~')

def hmacsha256(keyByte, message):
    return hmac.new(keyByte, message.encode('utf-8'), digestmod=hashlib.sha256).digest()


# Build a CanonicalRequest from a regular request string
#
# See
# http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html
# CanonicalRequest =
#  HTTPRequestMethod + '\n' +
#  CanonicalURI + '\n' +
#  CanonicalQueryString + '\n' +
#  CanonicalHeaders + '\n' +
#  SignedHeaders + '\n' +
#  HexEncode(Hash(RequestPayload))
def CanonicalRequest(r):
    if HeaderContentSha256 in r.headers.keys():
        hexencode = r.headers[HeaderContentSha256]
    else:
        if type(r.body)==bytes:
            hexencode = HexEncodeSHA256Hash(r.body)
        else:
            try:
                hexencode = HexEncodeSHA256Hash(r.body.encode('utf-8'))
            except:
                hexencode = HexEncodeSHA256Hash(r.body.decode('utf-8').encode('utf-8'))


    return "%s\n%s\n%s\n%s\n%s\n%s" % (
        r.method, CanonicalURI(r), CanonicalQueryString(r), CanonicalHeaders(r), SignedHeaders(r), hexencode)


def CanonicalURI(r):
    pattens = r.uri.split('/')
    uri = []
    for v in pattens:
        if v == "" or v == ".":
            continue
        elif v == '..':
            if len(uri) > 0:
                uri.pop()
        else:
            uri.append(urlencode(v))
    urlpath = "/"
    if len(uri) > 0:
        urlpath = urlpath + "/".join(uri) + "/"  # always end with /
    # r.uri = urlpath
    return urlpath


def CanonicalQueryString(r):
    a = []
    if type(r.query) == dict:
        for key in r.query:
            value = r.query[key]
            if value == "":
                kv = urlencode(key)
            else:
                # print(urlencode(key),urlencode(value))
                kv = urlencode(key) + "=" + str(urlencode(value))
            a.append(kv)
        a.sort()
        return '&'.join(a)
    else:
        from dis_sdk_python.com.huaweicloud.dis.sdk.python.proto import record_pb2
        target = record_pb2.GetRecordsRequest()
        target.ParseFromString(r.query)
        content = 'limit=' + str(target.limit) + '&' + 'partition-cursor=' + target.shardIterator
        return content


def CanonicalHeaders(r):
    a = []
    for key in r.headers:
        value = r.headers[key]
        keyEncoded = key.lower()
        a.append(keyEncoded + ":" + value.strip())
    a.sort()
    return '\n'.join(a) + "\n"


def SignedHeaders(r):
    a = []
    for key in r.headers:
        a.append(key.lower())
    a.sort()
    return ";".join(a)


# Return the Credential Scope. See http://docs.aws.amazon.com/general/latest/gr/sigv4-create-string-to-sign.html
def CredentialScope(t, Region, Service):
    return "%s/%s/%s/sdk_request" % (datetime.strftime(t, BasicDateFormatShort), Region, Service)


# Create a "String to Sign". See http://docs.aws.amazon.com/general/latest/gr/sigv4-create-string-to-sign.html
def StringToSign(canonicalRequest, credentialScope, t):
    sha256 = hashlib.sha256()
    sha256.update(canonicalRequest.encode('utf-8'))
    bytes = sha256.hexdigest()
    return "%s\n%s\n%s\n%s" % (Algorithm, datetime.strftime(t, BasicDateFormat), credentialScope, bytes)


# Generate a "signing key" to sign the "String To Sign". See http://docs.aws.amazon.com/general/latest/gr/sigv4-calculate-signature.html
def GenerateSigningKey(AppSecret, Region, Service, t):
    key = (PreSKString + AppSecret).encode('utf-8')
    dateStamp = datetime.strftime(t, BasicDateFormatShort)
    for d in [dateStamp, Region, Service, "sdk_request"]:
        key = hmacsha256(key, d)
        # print ("%s:%s" %(d, key.hex()))
    return key


# Create the HWS Signature. See http://docs.aws.amazon.com/general/latest/gr/sigv4-calculate-signature.html
def SignStringToSign(stringToSign, signingKey):
    hm = hmacsha256(signingKey, stringToSign)
    return binascii.hexlify(hm).decode()


# HexEncodeSHA256Hash returns hexcode of sha256
def HexEncodeSHA256Hash(body):
    sha256 = hashlib.sha256()
    sha256.update(body)
    return sha256.hexdigest()


# Get the finalized value for the "Authorization" header.  The signature
# parameter is the output from SignStringToSign
def AuthHeaderValue(signature, AppKey, credentialScope, signedHeaders):
    return "%s Credential=%s/%s, SignedHeaders=%s, Signature=%s" % (
        Algorithm, AppKey, credentialScope, signedHeaders, signature)


class SignerError(Exception):
    pass


class Signer:
    def __init__(self, ak, sk, region, serviceName="dis"):
        self.AppKey = ak
        self.AppSecret = sk
        self.Region = region
        self.Service = serviceName

    # SignRequest set Authorization header
    def Sign(self, r):
        # print(11,r.__dict__)
        headerTime = r.headers.get(HeaderXDate)
        if headerTime is None:
            t = datetime.utcnow()
            r.headers[HeaderXDate] = datetime.strftime(t, BasicDateFormat)
        else:
            t = datetime.strptime(headerTime, BasicDateFormat)

        if r.headers.get("host") is None:
            if r.host.split(':')[-1] == '443' or '80':
                r.host = r.host.split(':')[0]
            r.headers["host"] = r.host

        canonicalRequest = CanonicalRequest(r)
        # print ("canonicalRequest=%s" %(canonicalRequest))

        credentialScope = CredentialScope(t, self.Region, self.Service)
        # print ("credentialScope=%s" %(credentialScope))

        stringToSign = StringToSign(canonicalRequest, credentialScope, t)
        # print ("stringToSign=%s" %(stringToSign))

        key = GenerateSigningKey(self.AppSecret, self.Region, self.Service, t)
        # print ("key=%s" %(key.hex()))

        signature = SignStringToSign(stringToSign, key)
        # print ("signature=%s" %(signature))

        signedHeaders = SignedHeaders(r)
        authValue = AuthHeaderValue(signature, self.AppKey, credentialScope, signedHeaders)
        r.headers[HeaderAuthorization] = authValue
        r.headers["content-length"] = str(len(r.body))
        del r.headers["host"]
        '''
        queryString = CanonicalQueryString(r)
        if queryString != "":
            r.uri = r.uri + "?" + queryString
        '''
