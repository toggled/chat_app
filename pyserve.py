#-------------------------------------------------------------------------------
# Name:        pyserve.py
# Purpose:      A COMPLETE NETWORK PYTHON SERVER WHO SAVES THE FILE SENT BY THE CLIENT(pyclient.py)
# Issues:       serialization not implemented... so data not safe here
# Author:      andy
#
# Created:     10-12-2012
# Copyright:   (c) andy 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import socket,threading,os
host=''
port=10000
chunksize=4
var=3
def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(1)
    while True:
        try:
            sendersocket,sendaddr=s.accept()
            recvrsocket,recvaddr=s.accept()
        except:
            print 'error'
        #fileparameter management
        data=sendersocket.recv(4096)
        recvrsocket.sendall(data)
        print data.split('?')
        tag,filename,filesize=data.split('?')
        filesize=long(filesize)
        #
        '''
        #filename management
        i=1
        if(os.path.exists(filename+".saved")):
            name=filename+".saved"
            while(os.path.exists(name)):
                name=filename+str(i)+".saved"
                i+=1
            filename=name
        else:
            filename+=".saved"
        #


        try:
           fp=open(filename,'ab')
        except IOError:
                print 'File does not exist.'
                sys.exit(1)
'''
        received=long(0)
        while received<filesize:
            if received+chunksize<filesize:
                filedata=sendersocket.recv(chunksize)
                received+=chunksize
            else:
                filedata=sendersocket.recv(filesize-received)
                received+=(filesize-received)
            #print filedata
            recvrsocket.sendall(filedata)
            #print '%s bytes received' %received
        print "file closed"

        sendersocket.close()
        recvrsocket.close()
if __name__ == '__main__':
    	main()