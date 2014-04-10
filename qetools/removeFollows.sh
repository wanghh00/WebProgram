#!/bin/bash
for i in `cat testuserids.txt`
do
echo $i
./removeUserFollows.py $i
sleep 1
done
