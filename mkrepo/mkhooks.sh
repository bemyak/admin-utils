#!/bin/bash
# Создание хуков репозитория
svn_root=/opt/repo
svn_user=www-data
touch $svn_root/$1/hooks/pre-commit
echo '#!/bin/sh
'$svn_root'/.hooks/pre-commit $1 $2' $1 > $svn_root/$1/hooks/pre-commit
chmod a+x $svn_root/$1/hooks/pre-commit
touch $svn_root/$1/hooks/post-commit
echo '#!/bin/bash
'$svn_root'/.hooks/post-commit $1 $2 "_BPM_'$1'"' > $svn_root/$1/hooks/post-commit
chmod a+x $svn_root/$1/hooks/post-commit
chown -R $svn_user $svn_root/$1