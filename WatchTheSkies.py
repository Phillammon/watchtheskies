import sys
import os
import socket
import tarfile
import ARC

class IntentSocket(object):
    def __init__(self, port, targetport):
        targetip = str(sys.argv[1])
        self.filename = InterimFiles
        self.fileport = targetport + 1
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", port))
        self.sock.sendto("GIMME A VIDEO!", (targetip, targetport))
        print "Requesting images from " + targetip
    def Listen(self):
        reccommand, address = self.sock.recvfrom(1024)
        if isinstance(reccommand, str):
            if reccommand == "ON IT!":
                print "Images are being captured"
            elif reccommand == "RECORDED, CONVERTING!":
                print "Images captured, now welding"
            elif reccommand == "TO YOU!":
                print "Images welded successfully, downloading now."
                FileReciever = FileRecvSocket(self.fileport, (address[0], address[1]+1), self.filename)
                FileReciever.RecvFile()
                print "Image ArcWeld successfully downloaded. Hopefully."
                return True
        return False
        
class FileRecvSocket(object):
    def __init__(self, port, targetaddress, filename):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", port))
        self.sock.connect(targetaddress)
        self.file = open(filename + ".arc", "wb+")
        self.file.write("")
        self.file.close()
        self.file = open(filename + ".arc", "ab")
        self.filename = filename
    def RecvChunk(self, count):
        chunk = self.sock.recv(4096)
        print "Recieved Chunk #"+ str(count)
        return chunk
    def RecvFile(self):
        count = 0
        EOF = False
        while not EOF:
            count = count + 1
            chunk = self.RecvChunk(count)
            if chunk == "END OF FILE!":
                EOF = True
            else:
                self.file.write(chunk)
        self.file.close()
        self.sock.close()
def UnTar(filename):
    TarFile = tarfile.open(filename + ".tar")
    TarFile.extractall()
def UnWeld(filename):
    ARC.UnWeld(filename + ".arc", "./PPMImages", True, ".dng")
def WatchTheSkies():
    IntentionDeclarer = IntentSocket(31337, 31337)
    while not IntentionDeclarer.Listen():
        pass
    print "Unwelding images."
    UnTar(sys.argv[2])
    print "Done!"
    
WatchTheSkies()
