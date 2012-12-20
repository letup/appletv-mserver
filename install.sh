#!/bin/bash
/bin/cp cgi/* /usr/lib/cgi-bin
chown www-data.www-data /usr/lib/cgi-bin/*
chmod +x /usr/lib/cgi-bin/*
/bin/cp -f mbl/.htaccess /DataVolume/shares/.htaccess
mkdir -p /DataVolume/shares/Public/avs/pl/
/bin/cp -f mbl/.htaccess.pl /DataVolume/shares/Public/avs/pl/.htaccess
mkdir -p /opt/avs
/bin/cp -af mbl/* /opt/avs
/bin/cp -f server/* /opt/avs
chmod 755 /opt/avs/bin/*
chmod 755 /opt/avs/*.sh
chmod 755 /opt/avs/*.py
/bin/cp -f avs.sh /opt/avs/
chmod +x /opt/avs/avs.sh
ln -s /opt/avs/avs.sh /opt/etc/init.d/Savs.sh
ln -s /opt/avs/avs.sh /opt/etc/init.d/Kavs.sh
