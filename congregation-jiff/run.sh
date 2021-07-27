#!/bin/bash

python /app/decode_config.py
python /app/push_pull.py --pull
python /data/protocol.py /data/congregation_config.json
if [ $PID -eq 1 ]
then
	python /app/push_pull.py --push
fi