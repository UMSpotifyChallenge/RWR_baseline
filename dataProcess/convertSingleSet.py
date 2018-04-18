"""
Convert a prediction set into the pegasus numbering system
in: file path of file using songIDs
out: file of set using songNums


*** TELEPORT SETS ARE NOW ALWAYS IN PEG NUMBERING ***
"""

import sys
import pickle

songIDToSongNum = pickle.load( open( "songIDToSongNum.p", "rb" ) )

with open(sys.argv[1],"r") as inSet, open("pegTeleSet.txt",'w') as outSet:
    for line in inSet:
        line = line.strip()
        songID, restartWeight = line.split('\t')
        songNum = str(songIDToSongNum[songID])
        outSet.write(songNum +'\t'+ restartWeight +'\n')
