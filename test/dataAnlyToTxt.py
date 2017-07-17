#!/usr/bin/env python3

import sys
import re
from zlib import adler32

def fileWrite(file, data):
    for line in data:
        # Removes all unusual (\x00) characters, replaces with spaces
        line = ''.join([i if (ord(i) < 128 and ord(i) >= 32) else ' ' for i in line])
        # Removes excess whitespace
        line = ' '.join(line.split())
        lineSet = line.split()
        lineSet = line.split()
        try:
            if not (adler32(' '.join(lineSet[7:]).encode()) == int((lineSet[6]).replace(',',''))):
                pass # Confirming that checksum matches
        except:
            continue
        file.write(line + '\n')
    return

def readIn(dataFile, outFile):

    # Regular expression
    # \S{2} looks for two characters
    dwnlRe = re.compile(r'CU HE \S{2} ')
    
    with open(dataFile,'rb+') as f:
        raw = f.readlines()

    # In raw, each line counts as one character

    dwnlData = []

    for line in raw:
        str = line.decode(encoding='latin-1',errors='replace') 
        if len(str) > 150:
            continue
        if dwnlRe.search(str):
            dwnlData.append(str)# 237344 items 

    file = open(outFile,'w')
    fileWrite(file,dwnlData)
    file.close()
