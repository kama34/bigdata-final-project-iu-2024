#!/bin/bash
            
WORKING_DIR=/home/team8/project/bigdata-final-project-iu-2024

hdfs dfs -mkdir -p project/warehouse/avsc
hdfs dfs -put "$WORKING_DIR/output/"*.avsc /user/team8/project/warehouse/avsc