import random
import pickle

"""
This code will run RWR on entire dataset created by SpotifySynthesis
For now, no seperation between train/test. Just use all data for RWR
Steps:
	1. Relabel songIDs into songNums starting at 0
	2. Create an edge file with format: songNum \t songNum
After this program, the edge file will be fed into pegasus
"""

# songNum is labeling of the songs starting at 0
# songID is the id assinged in SpotifySynthesis
plistToSongNum = {}
songNumToSongID = {}
songIDToSongNum = {}
sNum = 0
songIDSet = set()

'''
Playlist_hypergraph format: songID \t playlistID
'''
with open("Playlist_hypergraph.txt","r") as f:
	for line in f:
		line = line.strip()
		songID, playID = line.split('\t')
		if playID not in plistToSongNum:
			plistToSongNum[playID] = []
		if songID not in songIDSet:
			songIDSet.add(songID)
			songNumToSongID[sNum] = songID
			songIDToSongNum[songID] = sNum
			sNum += 1
		plistToSongNum[playID].append( songIDToSongNum[songID] )


edgeList = []
with open('pegEdgeList.txt','w') as edgeF:
	for p in plistToSongNum.keys(): # for each playlist
		i1 = -1 # start with index of s1 at -1
		for s1 in plistToSongNum[p]: # for each song in the playlist, create an edge to other song
			i1+=1 # increment index of s1
			for s2 in plistToSongNum[p][i1+1:]: # for each song after s1
				edgeList.append( (str(s1),str(s2)) ) # create an edge between the songs

	random.shuffle(edgeList)

	for e in edgeList: # for 70% of the edges, put in train file
		edgeF.write(e[0]+'\t'+e[1]+'\n')


'''
add the info from the test set into these maps as well
'''
with open("playlistSplit/Playlist_TEST_graph.txt","r") as f:
	for line in f:
		line = line.strip()
		songID, playID = line.split('\t')
		if playID not in plistToSongNum:
			plistToSongNum[playID] = []
		if songID not in songIDSet:
			songIDSet.add(songID)
			songNumToSongID[sNum] = songID
			songIDToSongNum[songID] = sNum
			sNum += 1
		plistToSongNum[playID].append( songIDToSongNum[songID] )


## not sure if we need all 3 of these, but pickle them all anyway
pickle.dump( plistToSongNum, open( "plistToSongNum.p", "wb" ) )
pickle.dump( songNumToSongID, open( "songNumToSongID.p", "wb" ) )
pickle.dump( songIDToSongNum, open( "songIDToSongNum.p", "wb" ) )
