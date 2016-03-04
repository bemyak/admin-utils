#!/bin/bash
# Демонизация запуска JAR-файла
JAVA_HOME=$JAVA_HOME
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
JAR="MQStub-1.0-SNAPSHOT.jar"

if [ ! -f $DIR/$JAR ]; then
	echo "File not found!"
	echo "Please configure JAR variable inside the script or check file exists"
	exit 1;
fi

case "$1" in
start)
	if [ -f $DIR/.PID ]; then
                echo ".PID file found! Service seemes to be already started!"
                exit 1
        fi
	echo "Starting service..."
	nohup $JAVA_HOME/bin/java -jar $DIR/$JAR > $DIR/MQStub.log 2>> $DIR/MQStub.log < /dev/null &
	PID=$!
	echo $PID > $DIR/.PID
	echo "Done! PID is `cat $DIR/.PID`"
	exit 0;
	;;

stop)
	if [ ! -f $DIR/.PID ]; then
                echo "No .PID file found. Service seemes to be stoped"
                exit 1
	else
		if [ -f /proc/$PID/exe ]; then
			echo "Stoping service (PID `cat $DIR/.PID`)"
			PID=$(cat $DIR/.PID)
			kill $PID
			if [ -f /proc/$PID/exe ]; then
				echo "Something went wrong. Let's wait a little"
				sleep 1000
				if [ -f /proc/$PID/exe ]; then
					echo "Process is still alive! Sending SIGKILL. See log for details"
					kill -9 $PID
				fi
			fi
			if [ -f /proc/$PID/exe ]; then
				echo "I can't stop it! Sorry."
				exit 1
			else
				echo "Service stop successful."
				rm -rf $DIR/.PID
				exit 0;
			fi
		else
			echo "Process not found! Probably exeption occurs... Removing PID"
			rm -rf $DIR/.PID
		fi
	fi
	;;

status)
	if [ -f $DIR/.PID ]; then
		PID=$(cat $DIR/.PID)
		if [ -f /proc/$PID/exe ]; then
			echo "Service is running, PID is `cat $DIR/.PID`"
		else
			echo "Service is NOT running, but PID still exists. Seems exeption occurs. Removing PID"
			rm -rf $DIR/.PID
		fi
		exit 0;
	else
		echo "No .PID file found. Service seemes to be stoped"
		exit 0
	fi
	;;

force-stop)
	PID=$(cat $DIR/.PID)
	echo "Killing process `cat $DIR/.PID`"
	kill -9 $PID
	sleep 100
	if [ -f /proc/$PID/exe ]; then
		echo "I can't stop it! Sorry."
		exit 1	
        else
		echo "Process killed!"
		rm -rf $DIR/.PID
		exit 0
	fi
	;;

*)
	echo "Usage: MQStub.sh [start|stop|status|force-stop]"
	exit 0;
esac
