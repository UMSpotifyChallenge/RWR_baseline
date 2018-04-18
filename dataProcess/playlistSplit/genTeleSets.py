"""
CHANGE: NNOW ALL TELE_SETS ARE IN PEG NUMBERING SCHEME
"""

import pickle
import random
import sys
import os

if not os.path.exists("tele_sets"):
    os.makedirs("tele_sets")
if not os.path.exists("pred_sets"):
    os.makedirs("pred_sets")
if not os.path.exists("playlists"):
    os.makedirs("playlists")

songIDToSongNum = pickle.load(open("songIDToSongNum.p",'rb'))

## set ratio of what percentage of RWR should be in teleset. Remainder is in predset.
teleRatio = float(sys.argv[1]) # should be float between 0 and 1.0
plistToSongIDs = {}

with open("Playlist_TEST_graph.txt","r") as f:
    for line in f:
        line = line.strip()
        songID, playID = line.split('\t')
    	if playID not in plistToSongIDs:
    		plistToSongIDs[playID] = []
    	plistToSongIDs[playID].append( songID )

'''
Create a file with all songs in each playlist in comma seperated list {full playlist}
    line format: playlistNum\tsongID0,songID1,songID2,....
Create a set of files with sys.argv[1]% of songs in each playlist in comma seperated list {teleport set}
    line format: songID\trestartWeight
Create a set of files with (1-sys.argv[1])% of songs in each playlist in comma seperated list {set to predict}
    line format: songID\trestartWeight
'''
pNum = -1
for p in plistToSongIDs.keys(): # for each playlist
    pNum+=1
    random.shuffle(plistToSongIDs[p]) # shuffle the playlist randomly

    with open("tele_sets/tele_set_"+str(pNum),'w') as tset,\
    open("pred_sets/pred_set_"+str(pNum),'w') as pset,\
    open("playlists/plist_"+str(pNum),'w') as plist:
        for i in range(len(plistToSongIDs[p])):
            if i < teleRatio * len(plistToSongIDs[p]):
                songID = plistToSongIDs[p][i]
                songNum = songIDToSongNum[ songID ]
                tset.write(str(songNum)+'\t1\n') # uniform distribution of restart weights
            else:
                pset.write(str(plistToSongIDs[p][i])+'\t1\n') # uniform distribution of restart weights
            plist.write(str(plistToSongIDs[p][i])+'\n') # write all songs into playlist list
