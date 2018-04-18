#!/bin/bash

#alias hadoop="/home/drewdavi/Documents/598/proj/hadoop-2.9.0/bin/hadoop"
#alias hdfs"=/home/drewdavi/Documents/598/proj/hadoop-2.9.0/bin/hdfs"

#
#This shell will run RWR on entire dataset created by SpotifySynthesis
#to get the RWR results and use as the performance baseline
#Steps:
#	1. (py prog 1) Relabel songIDs into songNums starting at 0
#	2. (py prog 1) Create an edge file with format: songNum \t songNum
#  3. Submit edge file to pegasus
#  4. Save RWR scores and process into metrics?


rm -f pegEdgeList
python2.7 makeEdgeLists.py

hdfs dfs -rm -f pegEdgeList.txt
hdfs dfs -put pegEdgeList.txt
NUM_NODES=$( cat numOfNodes.txt )

hdfs dfs -rm -r -f tele_sets
hdfs dfs -mkdir tele_sets
hdfs dfs -put playlistSplit/tele_sets/* tele_sets/
rm -rf rwr_results
mkdir rwr_results
## Go through each teleport set and run PEGASUS RWR on it.
## Then save the RWR scores for later processing
for file in playlistSplit/tele_sets/*; do
  #hdfs dfs -rm -r -f rwr_vector/
  #rm -r -f rwr_vector/

  cd ../PEGASUS
  echo "Processing teleport set: ${file##*/}"
  ./run_rwr.sh pegEdgeList.txt tele_sets/${file##*/} ${NUM_NODES} 4 makesym new 0.75
  wait
  cd ../dataProcess

  # combine the rwr score results and move single file into a folder
  rm -rf rwr_vector
  hdfs dfs -get rwr_vector/
  cat rwr_vector/part-* >> rwr_vector/all_parts
  mv rwr_vector/all_parts rwr_results/${file##*/}_rwr_scores

done
