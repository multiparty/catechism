#!/bin/bash

python /app/push_pull.py --pull
python /data/protocol.py /data/congregation_config.json
python /app/push_pull.py --push
