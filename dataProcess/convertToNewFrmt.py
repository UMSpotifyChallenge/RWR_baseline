import random
import sys

plistToSongID = {}

with open("Playlist_hypergraph.txt",'r') as f:
	for line in f:
		line = line.strip()
		songID, plistID = line.split('\t')
		if plistID not in plistToSongID:
			plistToSongID[plistID] = []
		plistToSongID[plistID].append(songID)

with open('playlists_old.txt','w') as f:
	for p in plistToSongID.keys():
		f.write(p)
		for s in plistToSongID[p]:
			f.write(' '+ s)
		f.write('\n')
