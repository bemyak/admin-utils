#!/bin/bash
PASS=passowrd
wget --user SGureev --password $PASS http://fobos.lanit/guest/GenPSK.txt
smbclient //dibr-nas-001.lanit/\$CommonFolders\$/ $PASS -U SGureev -W LANIT -c 'cd Exchange; put GenPSK.txt WIFI-GUEST.txt; exit'
