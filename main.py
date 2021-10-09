import ftplib
import sys
import os
import time
import math

class FtpUploadTracker:
    sizeWritten = 0
    totalSize = 0
    lastShownPercent = 0
        
    def __init__(self, totalSize):
        self.totalSize = totalSize
    
    def handle(self, block):
        self.sizeWritten += 1024
        percentComplete = round((self.sizeWritten / self.totalSize) * 100)
        
        size1 = self.sizeWritten 
        total = self.totalSize
                
        def convert_size(size_bytes):
           if size_bytes == 0:
               return "0B"
           size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
           i = int(math.floor(math.log(size_bytes, 1024)))
           p = math.pow(1024, i)
           s = round(size_bytes / p, 2)
           return "%s %s" % (s, size_name[i])
        
        if (self.lastShownPercent != percentComplete):
            self.lastShownPercent = percentComplete
            b = str(percentComplete) + "%"
            
            print ("Upload... " + filename + "       " + b + "       {}/{}".format(convert_size(size1), convert_size(total)), end="\r")
            

ADDR = "ftp.1fichier.com"
USER = "" #EMAIL
PASS = "" #MDP

filename = sys.argv[1]
size = os.stat(filename).st_size

with open(filename, "rb") as file:
    uploadTracker = FtpUploadTracker(size)
    session = ftplib.FTP(ADDR,USER,PASS)             # file to send
    session.storbinary('STOR ' + filename, file, 1024, uploadTracker.handle )     # send the file
    file.close()                                    # close file and FTP
    session.quit()