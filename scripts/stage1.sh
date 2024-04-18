#!/bin/bash
echo "Stage1"

pip install gdown
url="https://drive.google.com/drive/folders/12B_yF8zr9pCPUFUupnR2Z_JUuEuuJ7qd"

gdown --folder $url -O data

rm data/README.txt


python3 scripts/csv_preprocess.py
python3 scripts/build_projectdb.py

bash scripts/hdfs_loader.sh

mv ./*java /home/team8/project/bigdata-final-project-iu-2024/output/
mv ./*avsc /home/team8/project/bigdata-final-project-iu-2024/output/