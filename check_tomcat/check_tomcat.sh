#!/bin/bash
# Проверяет, когда закончился запуск tomcat
#REM_HOST=sbld-cp-1.example.com
#REM_USER=was
#REM_PASS=was
#REM_PATH=/tmp/123
#LOG_NAME=catalina.out
#SUCCESS_TRIGGER="is completed"
#ERROR_TRIGGER="ERROR"
#TIMEOUT=5 #seconds

REM_HOST=$1
REM_USER=$2
REM_PASS=$3
REM_PATH=$4
LOG_NAME=$5
SUCCESS_TRIGGER=$6
ERROR_TRIGGER=$7
TIMEOUT=$8

#exit script if something fails (or exit status > 0)
#you should comment if for debug
set -e

trap "fusermount -u ~/.tmp/$$ && rm -rf ~/.tmp/$$" EXIT INT QUIT TERM
mkdir -p ~/.tmp/$$
sshfs -o password_stdin -o cache=no -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null $REM_USER@$REM_HOST:$REM_PATH ~/.tmp/$$ << EOL
$REM_PASS
EOL
timeout $TIMEOUT bash -c 'tail -n 0 -f ~/.tmp/$0/$1 | while read LOG_LINE; do
        [[ $LOG_LINE == *"$2"* ]] && pkill -P $$ tail && echo "success on $LOG_LINE" && exit 0 #SUCCESS
        [[ $LOG_LINE == *"$3"* ]] && pkill -P $$ tail && echo "error on $LOG_LINE" && exit 255 #ERROR
done' $$ "$LOG_NAME" "$SUCCESS_TRIGGER" "$ERROR_TRIGGER"
#script returns 124 on timeout
