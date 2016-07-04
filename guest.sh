#!/bin/bash
wget --user SGureev --password Segur\$78422 http://fobos.lanit/guest/GenPSK.txt
smbclient //dibr-nas-001.lanit/\$CommonFolders\$/ Segur\$78422 -U SGureev -W LANIT -c 'cd Exchange; put GenPSK.txt WIFI-GUEST.txt; exit'