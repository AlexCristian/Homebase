#! /bin/sh
PID_FILE="django.pid"
LOG_FILE="django.log"

if [ "$1" == "start" ]; then
	echo "" > "$LOG_FILE"
	sudo service postgresql start
	./manage.py runserver &>> "$LOG_FILE" &
	echo "$!" > $PID_FILE
	echo "Started deven."
elif [ "$1" == "stop" ]; then
	sudo service postgresql stop
	kill -- -$(ps -o pgid= $(cat "$PID_FILE") | grep -o '[0-9]*')
	rm "$PID_FILE"
	echo "Stopped devenv."
else
	echo "wut"
fi
	
