#!/bin/bash
LOGA="rand-agent.log"
(python3 random_agent.py -p 8023 &) >> $LOGA
sleep 2
LOG="rand.log"

for i in `seq 1 100`; do
        echo "---- Game $i ----"
        date -R
        echo -e "\n\n---- Game $i ----\n`date -R`\n\n" >> $LOG
        python3 game.py --no-gui http://localhost:8023 http://localhost:8023 >> $LOG-$i
        cat $LOG-$i >> $LOG
        sleep 1
done
