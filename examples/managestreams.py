#!/usr/bin/python
# -*- coding:utf-8 -*-


from dis import disclient
from dis import disresponse
from dis import disadminresponse

def test():
    #cli = disclient.disclient("endpoint",'ak', 'sk','projectid', 'region')
    cli = disclient.disclient("dis.cn-north-1.myhuaweicloud.com:20004",'ODO387IHGUPDQRH2BH6Z', '2xDa0FHfrzDKEooKogZrcghmdqBiWii5XjLCe3Ce','c159a24641da49b2a729ea6f57647888', 'cn-north-1')
    

    
    #streamName = "test_py1"
    try:

        r = cli.listStream()
        print (r._getStatusCode())
        streamList = r.streams
        print (streamList)
        '''
        for item in streamList:
            if item.isdigit():
                print (item)
                #r = cli.deleteStream(item)
                #print (r._getStatusCode())
                
        print ("end")

        #r = cli.describeStream(streamName)
        #r._printResponse()
        
        #r = cli.deleteStream(streamName)
        #print (r._getStatusCode())
     '''
    except Exception as ex:
        print (str(ex))



if __name__ == '__main__':
    print("hello world")
    test()