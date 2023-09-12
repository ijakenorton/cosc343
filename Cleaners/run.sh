#!/bin/bash
for i in 1 2 3 4; do
    cp 0/cleaners.py $i/
done


for i in 1 2 3 4; do
    cp 0/my_agent.py $i/
done

DISPLAY_NUM=99
LOCK_FILE="/tmp/.X${DISPLAY_NUM}-lock"

if [ ! -e "$LOCK_FILE" ]; then
    Xvfb :$DISPLAY_NUM &
else
    echo "X server is already running on display :$DISPLAY_NUM"
fi

for i in 0 1 2 3 4; do
    cd $i
    # Set the DISPLAY environment variable to use the virtual framebuffer
    DISPLAY=:99 python cleaners.py > /dev/null &
    cd ..
done

sleep 10
cd graphing
python graph2.py