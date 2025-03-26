#!/bin/bash
cd /home/ubuntu/SP25_DS5111_nms9dg
# log start
echo "Starting collection at $(date) for $1" >> collection_log.txt
#  make with TIME_OF_DAY parameter
make gainers SRC=yahoo TIME_OF_DAY=$1
make gainers SRC=wsj TIME_OF_DAY=$1
echo "Completed collection at $(date)" >> collection_log.txt
