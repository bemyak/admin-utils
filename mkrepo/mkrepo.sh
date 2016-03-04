#!/bin/bash
# Создание репозитория SVN
svn_root=/opt/repo
svn_user=www-data
svn_conf_file=/etc/apache2/sites-available/BPM-REPOS
/usr/bin/svnadmin create $svn_root/$1
/usr/bin/mkperms $1
sed -i "$ i <Location /"$1">\n\tDAV svn\n\tSVNPath "$svn_root"/"$1"\n\tAuthzSVNCrowdAccessFile "$svn_root""/""$1"/svn.authz\n\tRequire valid-user\n</Location>" $svn_conf_file
/usr/bin/mkhooks $1
service apache2 reload