#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Проверяет, есть ли просроченные дампы и отправляет уведомление на почту
# To get it work just:
# yum install MySQL-python
# or
# aptitude install python-mysqldb

import os
import sys
import socket
import subprocess
import datetime
import MySQLdb
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#######BASIC CONFIGURATION##################

db_host="zabbix.bpm.lanit"
db_user="dumpmon"
db_passwd="dumpmon"
db_name="dumpmon"
sender="dumpmon@bpm.lanit"
recievers=["_BPM_Admins@lanit.ru"]

############################################


#Connect to DB and execute test query

def send_notification_warn (sender,recievers, dump, schema, date, duedate):
	msg = MIMEMultipart('alternative')
	msg['Subject']='Истекает срок хранения дампа %s!' % (dump)
	msg['From']=sender
	msg['Content-Type'] = 'text/html; charset=utf-8'
	msg['To']=", ".join(recievers)
	text="""К сожалению, срок хранения дампа <b>%s</b> истёк. Вы получили это письмо, так как указаны в качестве отвественного сотрудника.<br>
Если потребность в дампе сохраняется, заведите задачу в <a href=http://jira.bpm.lanit>JIRA</a> на проект &#34;Поддержка&#34;  с просьбой изменить срок хранения. В противном случае, дамп будет удалён %s<br><br>
<table cellpadding=5 border=1>
<tr><td align=center colspan=2>Информация о дампе</td></tr>
<tr><td>Имя</td><td>%s</td></tr>
<tr><td>Схема</td><td>%s</td></tr>
<tr><td>Создан</td><td>%s</td></tr>
<tr><td>Окончание срока хранения</td><td>%s</td></tr>
</table>""" % (dump, duedate, dump, schema, date, duedate)
	part1 = MIMEText(text, 'html','utf-8')
	msg.attach(part1)
	s = smtplib.SMTP("post-m.lanit")
	s.sendmail(sender, recievers, msg.as_string() )
	s.quit()

def send_notification_del (sender,recievers,dump,id,ora_dir,host):
        msg = MIMEMultipart('alternative')
        msg['Subject']='Удалить дамп %s' % (dump)
        msg['From']=sender
        msg['Content-Type'] = 'text/html; charset=utf-8'
        msg['To']=", ".join(recievers)
        text="""Cрок хранения дампа <b>%s</b> истёк.<br>
Просьба сотрудников отдела удалть дамп.<br><br>
<table cellpadding=5 border=1>
<tr><td align=center colspan=2>Информация о дампе</td></tr>
<tr><td>ID</td><td>%s</td></tr>
<tr><td>NAME</td><td>%s</td></tr>
<tr><td>ORA_DIR</td><td>%s</td></tr>
<tr><td>HOST</td><td>%s</td></tr>
</table>""" % (dump, id, dump, ora_dir, host)
        part1 = MIMEText(text, 'html','utf-8')
        msg.attach(part1)
        s = smtplib.SMTP("post-m.lanit")
        s.sendmail(sender, recievers, msg.as_string() )
        s.quit()

################MAIN FUNCTION##############
try:
        db = MySQLdb.connect (db_host,db_user,db_passwd,db_name)
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT 1;")
except MySQLdb.OperationalError, err:
        print 'Can not connect to Database\n', err
        sys.exit(0)
 
#Check dumps to be deleted


cur.execute ("SELECT * FROM dumps WHERE duedate<=NOW();")
if cur.rowcount != 0:
	rows=cur.fetchall()
	for row in rows:
		reciever_list=list(recievers)
		reciever_list.append(row["ref"])
		print reciever_list
		send_notification_del (sender, reciever_list, row["name"], row["id"], row["ora_dir"], row["host"])

#Check dump to be soon deleted
cur.execute ("SELECT * FROM dumps WHERE duedate <= DATE_ADD(CURDATE(), INTERVAL 5 DAY) AND duedate>NOW();")
if cur.rowcount != 0:
        rows=cur.fetchall()
        for row in rows:
		reciever_list=list(recievers)
                reciever_list.append(row["ref"])
                send_notification_warn (sender, reciever_list, row["name"], row["schema"], row["name"], row["duedate"])
db.close()