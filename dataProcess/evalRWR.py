"""
Given a teleport set, prediciton set, and the RWR vector, evaluate how
good the RWR scores were.
A prediction is counted as correct when a song from the prediction set
appears in the top #% scores of the RWR rankings

Tele sets and pred sets are stored using original song IDs. So brings scores
back to original song IDs here as well

sys.argv[1] = num of tracks in this set
"""

import sys
import pickle
from os import listdir
import pdb
import random

track_counts = int(sys.argv[1])

songNumToSongID = pickle.load(open("songNumToSongID.p",'rb'))
songIDToSongNum = pickle.load(open("songIDToSongNum.p",'rb'))
result_per_pl = []

files = [f for f in listdir("./res_sets/")]
for path in files:

    scoreList = []
    _,_,setNumStr,_,_ = path.split('_')
    int(setNumStr) # just a type check

    print("Evaluating " + str(path))

    with open("./pred_sets/pred_set_"+setNumStr, 'r') as predSet, open("./res_sets/"+path, 'r') as resSet:
        resSetLineCount = 0
        for line in resSet:
            resSetLineCount += 1
            line = line.strip()
            songNum, songScore = line.split('\t')
            songScore = float(songScore[1:]) # remove 'v' and convert to a float for sorting
            ssTup = (songScore,songNumToSongID[int(songNum)]) # tuple of songScore, songID
            scoreList.append(ssTup)

        if resSetLineCount == 0: # if this is an empty res set, ignore it
            continue

        scoreList.sort(reverse=True) # sort scoreList by increasing score value

        songIDs = []
        for i in range(len(scoreList)):
            songIDs.append(scoreList[i][1]) # make a list with same order of just song IDs


        correctPredCount = 0
        predSetLength = 0
        correctSongIDs = []

        cond_top500 = int(500.0)
        cond_top01p = int(track_counts * 0.01)
        cond_top02p = int(track_counts * 0.025)
        cond_top05p = int(track_counts * 0.05)
        cond_top10p = int(track_counts * 0.10)

        per_pl_top500_count = 0
        per_pl_top01p_count = 0
        per_pl_top02p_count = 0
        per_pl_top05p_count = 0
        per_pl_top10p_count = 0

        for line in predSet:
            predSetLength += 1
            line = line.strip()
            songID, _ = line.split('\t')
            if songID in songIDs[:cond_top500]:
                per_pl_top500_count += 1
            if songID in songIDs[:cond_top01p]:
                per_pl_top01p_count += 1
            if songID in songIDs[:cond_top02p]:
                per_pl_top02p_count += 1
            if songID in songIDs[:cond_top05p]:
                per_pl_top05p_count += 1
            if songID in songIDs[:cond_top10p]:
                per_pl_top10p_count += 1

        result = []
        result.append(float(per_pl_top500_count) / predSetLength * 100)
        result.append(float(per_pl_top01p_count) / predSetLength * 100)
        result.append(float(per_pl_top02p_count) / predSetLength * 100)
        result.append(float(per_pl_top05p_count) / predSetLength * 100)
        result.append(float(per_pl_top10p_count) / predSetLength * 100)

        result_per_pl.append(result)


# save results in eval_results/ directory
with open("eval_results", 'w') as evalOut:
    #pdb.set_trace()
    for r in result_per_pl:
        for i in r:
            evalOut.write(str(i)+',')
        evalOut.write('\n')
