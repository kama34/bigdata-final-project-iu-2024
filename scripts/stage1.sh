#!/bin/bash

python3 scripts/csv_preprocess.py
python3 scripts/build_projectdb.py

bash scripts/hdfs_loader.sh

mv ./*java /home/team8/project/bigdata-final-project-iu-2024/output/
mv ./*avsc /home/team8/project/bigdata-final-project-iu-2024/output/