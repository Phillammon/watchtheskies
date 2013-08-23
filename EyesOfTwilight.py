import subprocess
import socket
import select
import time
import os
import ARC

class IntentSocket(object):
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", port))
        self.filesendport = port + 1
    def Listen(self, filename):
        reccommand, address = self.sock.recvfrom(1024)
        if isinstance(reccommand, str):
            if reccommand == "GIMME A VIDEO!":
                print "Recieved Request from " + address[0]
                self.sock.sendto("ON IT!", address)
                TakeImages(filename)
                self.sock.sendto("RECORDED, CONVERTING!", address)
                print "Extracting Raw Images"
                ExtractRAWs()
                print "Raw Images Extracted, Packaging as ArcWeld"
                WeldImages()
                print "Images Packaged, sending to " + address[0]
                self.sock.sendto("TO YOU!", address)
                FileSender = FileSendSocket(self.filesendport, "EyesOfTwilightImages.arc")
                FileSender.SendFile()
                print "Cleaning up"
                Process = subprocess.Popen("rm ./images/*", shell = True)
                Process.wait()
                print "Cleaned up, reopening to new requests"       
            
class FileSendSocket(object):
    def __init__(self, port, filename):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", port))
        self.file = open(filename, "rb")
        self.sock.listen(5)
        self.sock, dontcareaboutthis = self.sock.accept()
    def ReadChunk(self, size):
        return self.file.read(size)
    def SendFile(self):
        EOF = False
        count = 0
        while not EOF:
            chunk = self.ReadChunk(4096)
            count = count + 1
            if not chunk:
                EOF = True
                self.sock.sendall("END OF FILE!")
                print "Sent file chunk #" + str(count)
                print "File Sent"
            else:
                self.sock.sendall(chunk)
                print "Sent file chunk #" + str(count)
        self.file.close()
        self.sock.close()
def ExtractRAWs():
    imageslist = os.listdir('./images')
    Process = subprocess.Popen("cp ./raspi_dng ./images/", shell = True)
    Process.wait()
    counter = 0
    for image in imageslist:
        counter = counter + 1
        print "Extracting Raw #" + str(counter)
        Process = subprocess.Popen('./raspi_dng ./images/' + image + ' ./images/rawimage' + str(counter) + '.dng', shell = True)
        Process.wait()
        print "Extracted Raw #" + str(counter)
    Process = subprocess.Popen("cd ..", shell = True)
    Process.wait()
    Process = subprocess.Popen("rm ./images/raspi_dng", shell = True)
    Process.wait()
    print imageslist
def TarImages():
    Process = subprocess.Popen("tar -cvf EyesOfTwilightImages.tar ./images", shell = True)
    Process.wait()
def WeldImages():
    ARC.Weld([], "./images", "EyesOfTwilightImages.arc", 0)
def TakeImages(filename):
    for count in range(100):
        print "Taking Picture #" + str(count + 1)
        Process = subprocess.Popen("raspistill -t 1 -w 60 -h 40 -r -n -o ./images/" + filename + str(count) +".jpg -e jpg", shell = True)
        Process.wait()

def EyesOfTwilight():
    IntentDiviner = IntentSocket(31337)
    while True:
        IntentDiviner.Listen("EyesOfTwilightVideo")
EyesOfTwilight()
