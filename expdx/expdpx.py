#!/usr/bin/python2
# To get it work just:
# yum install MySQL-python
# Надстройка над expdpx, добавляет запись о дампе в БД

import os
import sys
import socket
import subprocess
import datetime
import MySQLdb

db_host="zabbix.bpm.lanit"
db_user="dumpmon"
db_passwd="dumpmon"
db_name="dumpmon"

#Connect to DB and execute test query
try:
        db = MySQLdb.connect (db_host,db_user,db_passwd,db_name)
        cur = db.cursor()
        cur.execute("SELECT 1;")
except MySQLdb.OperationalError, err:
        print 'Can not connect to Database\n', err
        sys.exit(0)
 
#Check if table exists, if not -- create one
try:
        cur.execute("SELECT 1 FROM dumps LIMIT 1;")
except MySQLdb.ProgrammingError:
        cur.execute ("CREATE TABLE `dumps`(`id` INT (11) NOT NULL AUTO_INCREMENT,`name` CHAR(255),`ora_dir` CHAR(255), `date` DATETIME, `duedate` DATE, `ref` CHAR(255), `cmd` TEXT, `host` CHAR(255), `schema` CHAR(255), PRIMARY KEY (`id`));")
        
#Locate expdp
oracle=os.getenv('ORACLE_HOME',0)
if oracle == 0:
        print 'No ORACLE_HOME!'
        sys.exit(0)
else:
        expdp=oracle+'/bin/expdp'
        
#Read arguments
args=sys.argv[1:]
duedate=""
ref=""
name=""
ora_dir=""
schema=""
for i in args[:]:
        if "duedate=" in i:
                duedate=i.split("=",1)[1]
                args.remove(i)
        elif "ref=" in i:
                ref=i.split("=",1)[1]
                args.remove(i)
        elif "dumpfile=" in i:
                name=i.split("=",1)[1]
        elif "directory=" in i:
                ora_dir=i.split("=",1)[1]
	elif "=" not in i and i != "expdp":
		schema=i.split("/",1)[0]
exit=0
if duedate=="":
        print 'No duedate specified! Please add ex. "duedate=16.04.2035" to your args'
        exit=1
if ref=="" or "@" not in ref:
        print 'No reference specified! Please, add email ex. "ref=somebody@bpm.lanit" to your args'
        exit=1
if exit==1:
        sys.exit(0)
cmd=' '.join(args)

#Execute oracle's expdp
try:
        subprocess.check_call ([expdp, cmd])
except KeyboardInterrupt, err:
        print err
except subprocess.CalledProcessError:
        print "expdp process return error. Aborting..."
        sys.exit(0)
        
#Insert data into table
try:
        cur.execute ("""INSERT INTO dumps (name,ora_dir,date,duedate,ref,cmd,host,`schema`) VALUES (%s,%s,NOW(),STR_TO_DATE(%s,'%%d.%%m.%%Y'),%s,%s,%s,%s);""",(name,ora_dir,duedate,ref,"expdp "+cmd,socket.gethostname(),schema))
        db.commit()
except:
        db.rollback()
        print "Can't INSERT INTO. Something wrong"
        raise
db.close()