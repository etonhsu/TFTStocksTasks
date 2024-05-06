#!/bin/bash
python ./tasks/lp_delta.py &
python ./tasks/portfolio_history.py &
python ./tasks/rank_update.py &
python ./tasks/riot_api.py &
wait
