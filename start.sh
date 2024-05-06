#!/bin/bash

export PYTHONPATH="$PWD:$PYTHONPATH"

python ./tasks/lp_delta.py > logs/lp_delta.log 2>&1 &
python ./tasks/portfolio_history.py > logs/portfolio_history.log 2>&1 &
python ./tasks/rank_update.py > logs/rank_update.log 2>&1 &
python ./tasks/riot_api.py > logs/riot_api.log 2>&1 &

wait
