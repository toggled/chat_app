#-------------------------------------------------------------------------------
# Name:        pyclient.py
# Purpose:      A COMPLETE NETWORK CLIENT WHO SENDS A FILE TO THE SERVER(pyserve.py)
# Issues:       serialization not implemented... so data not safe here
# Author:      andy
#
# Created:     10-12-2012
# Copyright:   (c) andy 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import socket,threading,os
host=socket.gethostbyaddr("127.0.0.1")[0]
port=10000
chunksize=4
def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    try:
        s.connect((host,port))
    except:
        print "Unable to connect to %s. Check the server." %host
        sys.exit(1)
    option=raw_input('send/receive')
    if option=='send':

        filename=os.path.abspath(raw_input('enter filename'))
        filesize=os.path.getsize(filename)
        print filesize
        s.send("file"+"?"+filename+"?"+str(filesize))
        try:
            with open(filename,'rb') as fp:
                while 1:
                    data=fp.read(chunksize)
                    #print data
                    s.sendall(data)
                    if len(data)==0:
                        print 'file sent successfully'
                        break

        except IOError:
            print 'File does not exist.'
            sys.exit(1)

        s.close()
    else:
        header=s.recv(4096)
        print header.split('?')
        tag,filename,filesize=header.split('?')
        filesize=long(filesize)
        i=1
        if(os.path.exists(filename+".client")):
            name=filename+".client"
            while(os.path.exists(name)):
                name=filename+str(i)+".client"
                i+=1
            filename=name
        else:
            filename+=".client"
        #
        received=long(0)
        try:
           fp=open(filename,'ab')
        except IOError:
                print 'File does not exist.'
                sys.exit(1)

        while received<filesize:
            if received+chunksize<filesize:
                filedata=s.recv(chunksize)
                received+=chunksize
            else:
                filedata=s.recv(filesize-received)
                received+=(filesize-received)
            #print filedata
            fp.write(filedata)
            #print '%s bytes received' %received

        fp.close()
        print "file closed"
        s.close()
if __name__ == '__main__':
    	main()