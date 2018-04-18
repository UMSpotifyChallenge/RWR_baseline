"""
Format of how playlists are represented changed from synthetic data to real data
This file converts from new (real) format to old (synthetic data)

new format:
playlistNumber0 s0 s1 s2 s3 ....\n
playlistNumber1 s2 s3 s6 s9 ....\n

old format:
songID0\tplaylistID8
songID1\tplaylistID8
"""
import sys

trainRatio = float(sys.argv[1]) # The percentage of playlists to use to build the graph

plistCount = 0
songToPlistDict = {} # map from songID -> list of playlist IDs
totalNumOfPlists = sum(1 for line in open('playlists_1000.txt'))
print("total num plists" + str(totalNumOfPlists))

with open("playlists_1000.txt",'r') as inF:
    for line in inF:
        plistCount += 1
        if plistCount > trainRatio * totalNumOfPlists:
            break
        line = line.strip()
        plistID, songIDlist = line.split(' ',1)
        for s in songIDlist.split(' '):
            if s not in songToPlistDict:
                songToPlistDict[s] = []
            songToPlistDict[s].append(plistID)

with open("Playlist_hypergraph.txt",'w') as outF:
    for s in songToPlistDict.keys():
        for p in songToPlistDict[s]:
            outF.write(s +'\t'+ p +'\n')



test_plistCount = 0
test_songToPlistDict = {}
with open("playlists_1000.txt",'r') as inF:
    for line in inF:
        test_plistCount += 1

        ## ignore all playlists already in graph
        if test_plistCount < trainRatio * totalNumOfPlists:
            continue

        line = line.strip()
        plistID, songIDlist = line.split(' ',1)
        for s in songIDlist.split(' '):
            if s not in test_songToPlistDict:
                test_songToPlistDict[s] = []
            test_songToPlistDict[s].append(plistID)

with open("playlistSplit/Playlist_TEST_graph.txt",'w') as outF:
    for s in test_songToPlistDict.keys():
        for p in test_songToPlistDict[s]:
            outF.write(s +'\t'+ p +'\n')

allSongs = {} # number of keys = number of songs
allSongs.update(songToPlistDict)
allSongs.update(test_songToPlistDict)
with open('numOfNodes.txt','w') as nodeNumF:
	nodeNumF.write(str(len(allSongs.keys())))
