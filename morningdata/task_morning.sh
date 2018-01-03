#!/usr/bin/env bash
source ~/.profile

MORNINGDATA_HOME=$(cd `dirname $0`; pwd)

python3 ${MORNINGDATA_HOME}/news_cj.py
python3 ${MORNINGDATA_HOME}/index_real_time.py