#!/usr/bin/python
# -*- coding: cp437 -*-

""" ARC Multifile Compression Format Implementation

Hooray for competing standards! The ARC compression format takes the average
(One of Mean, Median, Mode-Mean or Mode-Median) value of each byte of a set
of files, then records the differences between the average bytes and the actual
bytes
"""

import os

def Weld(fileslist = [], filesdirectory = "./", targetfile = "welded.arc", averagetype = 0): 
    """Welds together the target files into a single .arc file
    Fileslist argument is a list of the filenames of the files to be welded
    (filenames should be provided in string format)
    If no files are provided, all files in the dircetory filesdirectory are
    used instead. Format as string.
    Targetfile argument is used as the output file. Format as string.
    Averagetype chooses the method used for determining averages.
    0 = Modal Value. If there is no Modal Value, the Median is taken.
    1 = Modal Value. If there is no Modal Value, the Mean is taken.
    2 = Median Value
    3 = Mean Value"""
    binarylist = _GetBinary('A')+ _GetBinary('R')+ _GetBinary('C')+ _GetBinary('#')
    if fileslist == []:
        tempfileslist = os.listdir(filesdirectory)
        for item in tempfileslist:
            fileslist.append(filesdirectory + '/' + item)
    readfiles = []
    for filename in fileslist:
        if __name__ == "__main__":
            print "Reading File " + filename
        readfiles.append(_ReadFile(filename))
    longestfile = 0
    filelengths = []
    if __name__ == "__main__":
        print "Getting file lengths"
    for file in readfiles:
        lengthstring = str(len(file)/8)
        for char in lengthstring:
            binarylist = binarylist + _GetBinary(char)
        binarylist = binarylist + _GetBinary('#')
        if int(lengthstring) > longestfile:
            longestfile = int(lengthstring)
        filelengths.append(int(lengthstring))
    binarylist = binarylist + _GetBinary('#')
    AveragedFile = []
    FullValues = []
    if __name__ == "__main__":
        print "Averaging Values"
    if averagetype == 0:
        for pointer in range(longestfile):
            valuelist = []
            for file in readfiles:
                try:
                    valuelist.append(_GetDecimal(_GetFirstByte(file)))
                except:
                    pass
            AveragedFile.append(_ModalAverage(valuelist, True))
            FullValues.append(valuelist)
    if averagetype == 1:
        for pointer in range(longestfile):
            valuelist = []
            for file in readfiles:
                try:
                    valuelist.append(_GetDecimal(_GetFirstByte(file)))
                except:
                    pass
            AveragedFile.append(_ModalAverage(valuelist, False))
    if averagetype == 2:
        for pointer in range(longestfile):
            valuelist = []
            for file in readfiles:
                try:
                    valuelist.append(_GetDecimal(_GetFirstByte(file)))
                except:
                    pass
            AveragedFile.append(_MedianAverage(valuelist))
            FullValues.append(valuelist)
    if averagetype == 3:
        for pointer in range(longestfile):
            valuelist = []
            for file in readfiles:
                try:
                    valuelist.append(_GetDecimal(_GetFirstByte(file)))
                except:
                    pass
            AveragedFile.append(_MeanAverage(valuelist))
            FullValues.append(valuelist)
    for value in AveragedFile:
        binarylist = binarylist + _GetDecToBin(value, 8)
    if __name__ == "__main__":
        print "Getting Differences"
    for file in filelengths:
        for pointer in range(file):
            value = FullValues[pointer].pop(0)
            difference = value - AveragedFile[pointer]
            if difference < -7 or difference > 7:
                binarylist = binarylist + _GetDecToBin(8, 4)
                binarylist = binarylist + _GetDecToBin(value, 8)
            elif difference < 0:
                binarylist = binarylist + _GetDecToBin(difference + 16, 4)
            elif difference > 0:
                binarylist = binarylist + _GetDecToBin(difference, 4)
            else:
                binarylist = binarylist + _GetDecToBin(0, 4)
    if __name__ == "__main__":
        print "Writing File"
    _WriteFile(binarylist, targetfile)
    if __name__ == "__main__":
        print "Weld Complete"


def UnWeld(filename = "", targetdirectory = "./", createdirectory = False, suffix = ""): 
    """Unwelds a .arc file into the target directory
    Filename is the name of the .arc file to be unwelded. Format as string.
    Targetdirectory gives directory to Unweld files to. Format as string.
    If createdirectory is set to True, the targetdirectory will be created
    before Unwelding.
    If suffix is set, this file suffix will be added to the end of all UnWelded Files"""
    filebinary = _ReadFile(filename)
#   Confirm file type
    magicword = _GetCharacter(_GetFirstByte(filebinary)) + _GetCharacter(_GetFirstByte(filebinary)) + _GetCharacter(_GetFirstByte(filebinary)) 
    if magicword <> "ARC":
        raise ValueError("File given is not a .arc file")
    else:
        _GetFirstByte(filebinary)
    EOFL = False
    FileLengths = []
    LongestFile = 0
    while not EOFL:
        firstbyte = _GetCharacter(_GetFirstByte(filebinary))
        if firstbyte == "#":
            EOFL = True
        else:
            EON = False
            while not EON:
                byte = _GetCharacter(_GetFirstByte(filebinary))
                if byte == "#":
                    EON = True
                else:
                    firstbyte = firstbyte + byte
            FileLengths.append(int(firstbyte))
            if int(firstbyte) > LongestFile:
                LongestFile = int(firstbyte)
    AveragedFile = []
    for counter in range(LongestFile):
       AveragedFile.append(_GetDecimal(_GetFirstByte(filebinary)))
    filename = -1
    if createdirectory:
        try:
            os.mkdir(targetdirectory)
        except:
            pass
    for file in FileLengths:
        filename = filename + 1
        NewFileBinary = []
        for counter in range(file):
            difference = (_GetDecimal(_GetFirstNybble(filebinary)))
            if difference == 0:
                NewFileBinary = NewFileBinary + _GetDecToBin(AveragedFile[counter], 8)
            elif difference < 8:
                NewFileBinary = NewFileBinary + _GetDecToBin(AveragedFile[counter] + difference, 8)
            elif difference > 8:
                NewFileBinary = NewFileBinary + _GetDecToBin(AveragedFile[counter] + difference - 16, 8)
            else:
                NewFileBinary = NewFileBinary + _GetFirstByte(filebinary)
        _WriteFile(NewFileBinary, targetdirectory + "/" + str(filename).zfill(7) + suffix) 
    
    

"""Averaging"""

def _ModalAverage(list, defermedian = True):
    numdict = {}
    for item in list:
        if item in numdict.keys():
            numdict[item] = numdict[item] + 1
        else:
            numdict[item] = 1
    inverteddict = [(value, key) for key, value in numdict.items()]
    modaltuple = max(inverteddict)
    if modaltuple[0] == 1:
        if defermedian:
            return _MedianAverage(list)
        else:
            return _MeanAverage(list)
    return modaltuple[1]
    
def _MedianAverage(list):
    sortedlist = sorted(list)
    listitems = len(sortedlist)
    if not listitems % 2:
        return (sortedlist[listitems / 2] + sortedlist[listitems / 2 - 1]) / 2.0
    return sortedlist[listitems / 2]

def _MeanAverage(list):
    listitems = len(list)
    total = 0
    for item in list:
        total = total + item
    return int(total/listitems)
    
"""Binary Manipulation"""

def _GetCharacter(binarylist):
    decrep = 0
    multiple = 1
    binarylist.reverse()
    for digit in binarylist:
        if digit:
            decrep = decrep + multiple
        multiple = multiple * 2
    return chr(decrep)

def _GetDecimal(binarylist):
    decrep = 0
    multiple = 1
    binarylist.reverse()
    for digit in binarylist:
        if digit:
            decrep = decrep + multiple
        multiple = multiple * 2
    return decrep

def _GetBinary(character):
    binstring = bin(ord(character)).replace('0b', '')
    binstring = binstring.zfill(8)
    binlist = []
    for char in binstring:
        binlist.append(int(char))
    return binlist

def _GetDecToBin(value, digits):
    binstring = bin(int(value)).replace('0b', '')
    binstring = binstring.zfill(digits)
    binlist = []
    for char in binstring:
        binlist.append(int(char))
    return binlist

def _GetFirstByte(list):
    byte = []
    bitflag = False
    for i in range(8):
        try:
            byte.append(list.pop(0))
            bitflag = True
        except:
            if bitflag:
                byte.append(0)
            else:
                return byte
    return byte
def _GetFirstNybble(list):
    nybble = []
    bitflag = False
    for i in range(4):
        try:
            nybble.append(list.pop(0))
            bitflag = True
        except:
            if bitflag:
                nybble.append(0)
            else:
                return nybble
    return nybble
        

"""File Manipulation"""

def _ReadFile(filename):
    bitlist = []
    file = open(filename, "rb")
    for character in file.read():
        if __name__ == "__main__":
            print "Byte Read: " + character
        bitlist = bitlist + _GetBinary(character)
    file.close()
    return bitlist

def _WriteFile(bitlist, filename):
    EOF = False
    file = open(filename, 'wb+')
    while not EOF:
        binary = _GetFirstByte(bitlist)
        if binary == []:
            EOF = True
        else:
            file.write(_GetCharacter(binary))
    file.close()

"""Main Function"""

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="Chooses whether to weld or unweld. W welds, U unwelds.")
    parser.add_argument("filename", help="Name of .arc file to create/unweld")
    parser.add_argument("directory", help="Name of directory to weld/unweld to")
    parser.add_argument("-a", "--averagemode", help="Set type of average to use (0 to 3)", type = int)
    parser.add_argument("-c", "--createdirectory", help="If set, unwelding will create the required directory", action="store_true")
    parser.add_argument("-s", "--suffix", help="If set, unwelded files will use this file suffix")
    args = parser.parse_args()
    if args.mode == "u" or args.mode == "U":
        UnWeld(args.filename, args.directory, args.createdirectory, args.suffix)
    elif args.mode == "w" or args.mode == "W":
        Weld([], args.directory, args.filename, args.averagemode)
    else:
        raise ValueError("Mode not recognized")
